import asyncio
from uuid import UUID
from pydantic import ValidationError
from typing_extensions import override
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict, List, Optional, Union

# utils
from app.utils.response import DAOResponse

# enums
from app.schema.enums import ContractStatus

# daos
from app.dao.auth.user_dao import UserDAO
from app.dao.resources.base_dao import BaseDAO
from app.dao.resources.utilities_dao import UtilitiesDAO
from app.dao.billing.payment_type_dao import PaymentTypeDAO
from app.dao.contracts.contract_type_dao import ContractTypeDAO

# models
from app.models.contract import Contract
from app.models.under_contract import UnderContract

# schemas
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

        self.user_dao = UserDAO()
        self.utility_dao = UtilitiesDAO()
        self.payment_type_dao = PaymentTypeDAO()
        self.contract_type_dao = ContractTypeDAO()
        self.under_contract_dao = BaseDAO(UnderContract)

        self.detail_mappings = {
            "contract_info": self.add_contract_details,
            "utilities": self.utility_dao.add_entity_utility,
        }

        super().__init__(self.model, nesting_degree=nesting_degree, excludes=excludes)

    @override
    async def create(
        self,
        db_session: AsyncSession,
        obj_in: ContractCreateSchema,
    ) -> DAOResponse[ContractResponse]:
        try:
            contract_info = self.extract_model_data(
                self.exclude_keys(obj_in, ["contract_info"]),
                ContractBase,
            )

            # prepare contract information
            contract_info = await self.prepare_contract_info(
                db_session=db_session,
                contract_info=contract_info,
                contract_info_key="contract_info",
            )

            # create new contract
            new_contract: Contract = await super().create(
                db_session=db_session, obj_in=contract_info
            )

            # process any entity details
            await self.handle_entity_details(
                db_session=db_session,
                entity_data=obj_in,
                detail_mappings=self.detail_mappings,
                entity_model=self.model.__name__,
                entity_assoc_id=new_contract.contract_id,
                contract=new_contract,
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

        return DAOResponse[List[ContractResponse | Dict]](
            success=True, data=[ContractResponse.from_orm_model(r) for r in result]
        )

    @override
    async def get(
        self, db_session: AsyncSession, id: Union[UUID | Any | int]
    ) -> DAOResponse[ContractResponse]:
        result = await super().get(db_session=db_session, id=id)

        return DAOResponse[ContractResponse](
            success=bool(result),
            data={} if result is None else ContractResponse.from_orm_model(result),
        )

    @override
    async def update(
        self, db_session: AsyncSession, db_obj: Contract, obj_in: ContractUpdateSchema
    ) -> DAOResponse[ContractResponse]:
        try:
            contract_info = obj_in.model_dump(exclude=["contract_info", "utilities"])

            # prepare contract information
            contract_info = await self.prepare_contract_info(
                db_session=db_session,
                contract_info=contract_info,
                contract_info_key="contract_info",
            )

            # update contract info
            updated_contract = await super().update(
                db_session=db_session, db_obj=db_obj, obj_in=contract_info.items()
            )

            # process any entity details
            await self.handle_entity_details(
                db_session=db_session,
                entity_data=obj_in.model_dump(),
                detail_mappings=self.detail_mappings,
                entity_model=self.model.__name__,
                entity_assoc_id=updated_contract.contract_id,
                contract=updated_contract,
            )

            return DAOResponse(
                success=True, data=ContractResponse.from_orm_model(updated_contract)
            )
        except ValidationError as e:
            return DAOResponse(success=False, validation_error=str(e))
        except Exception as e:
            await db_session.rollback()
            return DAOResponse(success=False, error=f"Fatal Update {str(e)}")

    async def prepare_contract_info(
        self,
        db_session: AsyncSession,
        contract_info: Dict[str, Any],
        contract_info_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Helper method to prepare contract information by fetching contract type, payment type,
        and validating the contract status. Also, it validates nested IDs if necessary.
        """
        # fetch contract and payment types concurrently
        contract_type_task = self.contract_type_dao.get_existing_contract_type(
            db_session=db_session, contract_type=contract_info.get("contract_type")
        )
        payment_type_task = self.payment_type_dao.get_existing_payment_type(
            db_session=db_session, payment_type=contract_info.get("payment_type")
        )

        (
            contract_info["contract_type"],
            contract_info["payment_type"],
        ) = await asyncio.gather(contract_type_task, payment_type_task)

        # validate contract status
        if contract_info.get("contract_status") not in ContractStatus:
            raise NoResultFound("Contract status does not exist")
        else:
            contract_info["contract_status"] = ContractStatus(
                contract_info["contract_status"]
            )

        # Validate nested IDs and process entity details if present
        if contract_info_key and contract_info_key in contract_info:
            await self.validate_nested_ids(db_session, contract_info[contract_info_key])

        return contract_info

    async def validate_nested_ids(
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
                raise NoResultFound("Client or Employee ID does not exist")

    async def add_contract_details(
        self,
        db_session: AsyncSession,
        entity_id: str,
        contract_info: Union[UnderContractSchema | List[UnderContractSchema]],
        contract: Union[Contract | None] = None,
    ):
        try:
            contract_info = (
                contract_info if isinstance(contract_info, list) else [contract_info]
            )
            results = []

            for contract_item in contract_info:
                under_contract_obj = {
                    "property_unit_assoc_id": contract_item.property_unit_assoc,
                    "employee_id": contract_item.employee_id,
                    "client_id": contract_item.client_id,
                    "contract_status": contract_item.contract_status,
                    "contract_id": contract.contract_number,
                    "start_date": contract_item.start_date,
                    "end_date": contract_item.end_date,
                    "next_payment_due": contract_item.next_payment_due,
                }

                result = await self.create_or_update_contract_details(
                    db_session, under_contract_obj, contract_item
                )
                await self.commit_and_refresh(db_session, result)
                results.append(result)

            return results

        except ValidationError as e:
            return DAOResponse(success=False, validation_error=str(e))
        except Exception as e:
            return DAOResponse(success=False, error=f"Fatal {str(e)}")

    async def create_or_update_contract_details(
        self,
        db_session: AsyncSession,
        under_contract_obj: Dict[str, Any],
        contract_item: UnderContractSchema,
    ) -> Union[UnderContract | None]:
        existing_contract_details = await self.get_existing_contract_details(
            db_session=db_session, contract_item=contract_item
        )

        if existing_contract_details:
            return await self.under_contract_dao.update(
                db_session=db_session,
                db_obj=existing_contract_details,
                obj_in=under_contract_obj.items(),
            )
        else:
            return await self.under_contract_dao.create(
                db_session=db_session, obj_in=under_contract_obj
            )

    async def get_existing_contract_details(
        self, db_session: AsyncSession, contract_item: UnderContractSchema
    ):
        if "under_contract_id" in contract_item.model_fields:
            return await self.under_contract_dao.query(
                db_session=db_session,
                filters={"under_contract_id": contract_item.under_contract_id},
                single=True,
            )
        return None
