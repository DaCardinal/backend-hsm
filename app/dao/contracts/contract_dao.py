import asyncio
from uuid import UUID
from functools import partial
from pydantic import ValidationError
from typing_extensions import override
from typing import Any, Dict, List, Union
from sqlalchemy.ext.asyncio import AsyncSession

# utils
from app.dao.auth.user_dao import UserDAO
from app.utils.response import DAOResponse

# enums
from app.schema.enums import ContractStatus

# daos
from app.dao.resources.base_dao import BaseDAO
from app.dao.resources.utilities_dao import UtilitiesDAO
from app.dao.billing.payment_type_dao import PaymentTypeDAO
from app.dao.contracts.contract_type_dao import ContractTypeDAO

# models
from app.models.contract import Contract
from app.models.under_contract import UnderContract

# schemas
from app.schema.billable import EntityBillableCreate
from app.schema.mixins.contract_mixin import UnderContractSchema
from app.schema.contract import (
    ContractCreateSchema,
    ContractUpdateSchema,
    ContractResponse,
    ContractBase,
)


class ContractDAO(BaseDAO[Contract]):
    def __init__(self, excludes=[], nesting_degree: str = BaseDAO.IMMEDIATE_CHILD):
        self.model = Contract
        self.primary_key = "contract_number"
        self.utility_dao = UtilitiesDAO()
        self.payment_type_dao = PaymentTypeDAO()
        self.contract_type_dao = ContractTypeDAO()
        self.user_dao = UserDAO()
        self.under_contract_dao = BaseDAO(UnderContract)

        super().__init__(self.model, nesting_degree=nesting_degree, excludes=excludes)

    @override
    async def create(
        self, db_session: AsyncSession, obj_in: ContractCreateSchema
    ) -> DAOResponse[ContractResponse | Dict]:
        try:
            contract_info = self.extract_model_data(
                ContractCreateSchema(**obj_in).model_dump(exclude=["contract_info"]),
                ContractBase,
            )
            contract_type = contract_info.get("contract_type")
            payment_type = contract_info.get("payment_type")

            validation_response = await self._validate_ids(
                db_session, contract_type, payment_type
            )

            if not isinstance(validation_response, tuple) and validation_response:
                return validation_response

            contract_type_result, payment_type_result = validation_response
            contract_info["contract_type"] = contract_type_result
            contract_info["payment_type"] = payment_type_result

            if contract_info.get("contract_status") not in ContractStatus:
                return DAOResponse(
                    success=False, error="Contract status does not exist", data={}
                )

            new_contract = await super().create(
                db_session=db_session, obj_in=contract_info
            )

            details_methods = self._prepare_details_methods(new_contract)

            if "contract_info" in obj_in and obj_in["contract_info"]:
                contract_info_data = obj_in["contract_info"]

                validation_response = await self._validate_nested_ids(
                    db_session, contract_info_data
                )
                if validation_response:
                    return validation_response

            if set(details_methods.keys()) & set(obj_in.keys()):
                await self.process_entity_details(
                    db_session, new_contract.contract_id, obj_in, details_methods
                )

            await self.commit_and_refresh(db_session, new_contract)

            return DAOResponse(
                success=True, data=ContractResponse.from_orm_model(new_contract)
            )
        except ValidationError as e:
            return DAOResponse(success=False, data=str(e))
        except Exception as e:
            await db_session.rollback()
            return DAOResponse(success=False, error=f"Fatal {str(e)}")

    @override
    async def get_all(
        self, db_session: AsyncSession, offset=0, limit=100
    ) -> DAOResponse[List[ContractResponse]]:
        result = await super().get_all(
            db_session=db_session, offset=offset, limit=limit
        )

        if not result:
            return DAOResponse(success=True, data=[])

        return DAOResponse[List[ContractResponse | Dict]](
            success=True, data=[ContractResponse.from_orm_model(r) for r in result]
        )

    @override
    async def get(
        self, db_session: AsyncSession, id: Union[UUID | Any | int]
    ) -> DAOResponse[ContractResponse]:
        result = await super().get(db_session=db_session, id=id)

        if not result:
            return DAOResponse(success=True, data={})

        return DAOResponse[ContractResponse](
            success=True, data=ContractResponse.from_orm_model(result)
        )

    @override
    async def update(
        self, db_session: AsyncSession, db_obj: Contract, obj_in: ContractUpdateSchema
    ) -> DAOResponse[ContractResponse | Dict]:
        try:
            contract_info = obj_in.model_dump(exclude=["contract_info", "utilities"])
            contract_type = contract_info.get("contract_type")
            payment_type = contract_info.get("payment_type")

            validation_response = await self._validate_ids(
                db_session, contract_type, payment_type
            )

            if not isinstance(validation_response, tuple) and validation_response:
                return validation_response

            contract_type_result, payment_type_result = validation_response
            contract_info["payment_type"] = payment_type_result
            contract_info["contract_type"] = contract_type_result

            if contract_info.get("contract_status") not in ContractStatus:
                return DAOResponse(
                    success=False, error="Contract status does not exist", data={}
                )

            updated_contract = await super().update(
                db_session=db_session, db_obj=db_obj, obj_in=contract_info.items()
            )

            details_methods = self._prepare_details_methods(updated_contract)

            if "contract_info" in obj_in and obj_in["contract_info"]:
                contract_info_data = obj_in["contract_info"]
                validation_response = await self._validate_nested_ids(
                    db_session, contract_info_data
                )
                if validation_response:
                    return validation_response

            if set(details_methods.keys()).issubset(set(obj_in.model_dump().keys())):
                await self.process_entity_details(
                    db_session,
                    updated_contract.contract_number,
                    obj_in.model_dump(),
                    details_methods,
                )

            await self.commit_and_refresh(db_session, updated_contract)

            return DAOResponse(
                success=True, data=ContractResponse.from_orm_model(updated_contract)
            )
        except ValidationError as e:
            return DAOResponse(success=False, validation_error=str(e))
        except Exception as e:
            await db_session.rollback()
            return DAOResponse(success=False, error=f"Fatal Update {str(e)}")

    async def _validate_ids(
        self,
        db_session: AsyncSession,
        contract_type: str,
        payment_type: str,
    ) -> Union[None, DAOResponse]:
        contract_type_query = self.contract_type_dao.query(
            db_session, filters={"contract_type_name": contract_type}, single=True
        )
        payment_type_query = self.payment_type_dao.query(
            db_session, filters={"payment_type_name": payment_type}, single=True
        )

        contract_type_result, payment_type_result = await asyncio.gather(
            contract_type_query, payment_type_query
        )

        if not contract_type_result:
            return DAOResponse(
                success=False, error="Contract type does not exist", data={}
            )
        if not payment_type_result:
            return DAOResponse(
                success=False, error="Payment type does not exist", data={}
            )

        return (contract_type_result, payment_type_result)

    async def _validate_nested_ids(
        self,
        db_session: AsyncSession,
        contract_info: List[UnderContractSchema | Dict[str, Any]],
    ) -> Union[None, DAOResponse]:
        user_dao_queries = []
        for info in contract_info:
            user_dao_queries.append(
                self.user_dao.query(
                    db_session, filters={"user_id": info.get("client_id")}, single=True
                )
            )
            user_dao_queries.append(
                self.user_dao.query(
                    db_session,
                    filters={"user_id": info.get("employee_id")},
                    single=True,
                )
            )

        results = await asyncio.gather(*user_dao_queries)
        for result in results:
            if not result:
                return DAOResponse(
                    success=False, error="Client or Employee ID does not exist", data={}
                )

    def _prepare_details_methods(self, contract: Contract):
        return {
            "contract_info": (
                partial(self._add_contract_details, contract=contract),
                UnderContractSchema,
            ),
            "utilities": (
                partial(
                    self.utility_dao.add_entity_utility,
                    entity_model=self.model.__name__,
                    entity_assoc_id=contract.contract_id,
                ),
                EntityBillableCreate,
            ),
        }

    async def _add_contract_details(
        self,
        db_session: AsyncSession,
        contract_id: str,
        contract_info: UnderContractSchema,
        contract: Contract = None,
        under_contract: UnderContract = None,
    ):
        try:
            if not isinstance(contract_info, list):
                contract_info = [contract_info]

            for contract_item in contract_info:
                contract_item: UnderContractSchema = contract_item

                under_contract_obj = {
                    "property_unit_assoc_id": contract_item.property_unit_assoc,
                    "employee_id": contract_item.employee_id,
                    "client_id": contract_item.client_id,
                    "contract_status": contract.contract_status.name,
                    "contract_id": contract.contract_number,
                    "start_date": contract.start_date,
                    "end_date": contract_item.end_date,
                    "next_payment_due": contract_item.next_payment_due,
                }

                existing_contract_details = await self._get_existing_contract_details(
                    db_session, contract_item
                )

                if existing_contract_details:
                    contract_details = await self.under_contract_dao.update(
                        db_session=db_session,
                        db_obj=existing_contract_details,
                        obj_in=under_contract_obj.items(),
                    )
                else:
                    contract_details = await self.under_contract_dao.create(
                        db_session=db_session, obj_in=under_contract_obj
                    )

                await self.under_contract_dao.commit_and_refresh(
                    db_session, contract_details
                )

            return contract_details
        except ValidationError as e:
            return DAOResponse(success=False, validation_error=str(e))
        except Exception as e:
            return DAOResponse(success=False, error=f"Fatal {str(e)}")

    async def _get_existing_contract_details(
        self, db_session: AsyncSession, contract_item: UnderContractSchema
    ):
        if "under_contract_id" in contract_item.model_fields:
            return await self.under_contract_dao.query(
                db_session=db_session,
                filters={"under_contract_id": contract_item.under_contract_id},
                single=True,
            )
        return None
