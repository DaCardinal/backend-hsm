from uuid import UUID
from functools import partial
from pydantic import ValidationError
from typing_extensions import override
from typing import Any, Dict, List, Union
from sqlalchemy.ext.asyncio import AsyncSession

# utils
from app.utils.response import DAOResponse

# enums
from app.schema.enums import ContractStatus

# daos
from app.dao.resources.base_dao import BaseDAO
from app.dao.resources.utilities_dao import UtilitiesDAO
from app.dao.billing.payment_type_dao import PaymentTypeDAO
from app.dao.contracts.contract_type_dao import ContractTypeDAO

# models
from app.models.utility import Utilities
from app.models.contract import Contract
from app.models.payment_type import PaymentTypes
from app.models.contract_type import ContractType
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
        self.utility_dao = UtilitiesDAO(Utilities)
        self.payment_type_dao = PaymentTypeDAO(PaymentTypes)
        self.contract_type_dao = ContractTypeDAO(ContractType)

        super().__init__(self.model, nesting_degree=nesting_degree, excludes=excludes)

    @override
    async def create(
        self, db_session: AsyncSession, obj_in: ContractCreateSchema
    ) -> DAOResponse[ContractResponse | Dict]:
        try:
            # extract base information
            contract_info = self.extract_model_data(
                ContractCreateSchema(**obj_in).model_dump(exclude=["contract_info"]),
                ContractBase,
            )
            contract_type = contract_info.get("contract_type")
            contract_status = contract_info.get("contract_status")
            payement_type = contract_info.get("payment_type")

            # check if contract type exists
            existing_contract_type: ContractType = await self.contract_type_dao.query(
                db_session=db_session,
                filters={"contract_type_name": contract_type},
                single=True,
            )

            if not existing_contract_type:
                return DAOResponse(
                    success=False, error="Contract type does not exist", data={}
                )

            # check if contract status exists
            if contract_status not in ContractStatus:
                return DAOResponse(
                    success=False, error="Contract status does not exist", data={}
                )

            # set contract type id
            contract_info["contract_type"] = existing_contract_type

            # check if payment type exists
            existing_payment_type: PaymentTypes = await self.payment_type_dao.query(
                db_session=db_session,
                filters={"payment_type_name": payement_type},
                single=True,
            )

            if not existing_payment_type:
                return DAOResponse(
                    success=False, error="Payment type does not exist", data={}
                )

            # set payment type id
            contract_info["payment_type"] = existing_payment_type
            new_contract: Contract = await super().create(
                db_session=db_session, obj_in=contract_info
            )

            details_methods = {
                "contract_info": (
                    partial(self.add_contract_details, contract=new_contract),
                    UnderContractSchema,
                ),
                "utilities": (
                    partial(
                        self.utility_dao.add_entity_utility,
                        entity_model=self.model.__name__,
                        entity_assoc_id=new_contract.contract_id,
                    ),
                    EntityBillableCreate,
                ),
            }

            if set(details_methods.keys()).issubset(set(obj_in.keys())):
                await self.process_entity_details(
                    db_session, new_contract.contract_id, obj_in, details_methods
                )

            # commit object to db session
            await self.commit_and_refresh(db_session, new_contract)

            return DAOResponse[ContractResponse](
                success=True, data=ContractResponse.from_orm_model(new_contract)
            )
        except ValidationError as e:
            return DAOResponse(success=False, data=str(e))
        except Exception as e:
            await db_session.rollback()
            return DAOResponse[ContractResponse](success=False, error=f"Fatal {str(e)}")

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
            # get the entity dump info
            contract_info = obj_in.model_dump(exclude=["contract_info", "utilities"])

            contract_type = contract_info.get("contract_type")
            payement_type = contract_info.get("payment_type")

            # check if contract type exists
            existing_contract_type: ContractType = await self.contract_type_dao.query(
                db_session=db_session,
                filters={"contract_type_name": contract_type},
                single=True,
            )

            if not existing_contract_type:
                return DAOResponse(
                    success=False, error="Contract type does not exist", data={}
                )

            # set contract type id
            contract_info["contract_type"] = existing_contract_type

            # check if payment type exists
            existing_payment_type: PaymentTypes = await self.payment_type_dao.query(
                db_session=db_session,
                filters={"payment_type_name": payement_type},
                single=True,
            )

            if not existing_payment_type:
                return DAOResponse(
                    success=False, error="Payment type does not exist", data={}
                )

            # set payment type id
            contract_info["payment_type"] = existing_payment_type

            # update contract info
            existing_contract: Contract = await super().update(
                db_session=db_session, db_obj=db_obj, obj_in=contract_info.items()
            )

            # add additional info if exists | Determine the correct schema for the contract
            details_methods = {
                "contract_info": (
                    partial(self.add_contract_details, contract=existing_contract),
                    UnderContractSchema,
                ),
                "utilities": (
                    partial(
                        self.utility_dao.add_entity_utility,
                        entity_model=self.model.__name__,
                        entity_assoc_id=existing_contract.contract_id,
                    ),
                    EntityBillableCreate,
                ),
            }

            # add additional info if exists
            if set(details_methods.keys()).issubset(set(obj_in.model_dump().keys())):
                await self.process_entity_details(
                    db_session,
                    existing_contract.contract_id,
                    obj_in.model_dump(),
                    details_methods,
                )

            # commit object to db session
            await self.commit_and_refresh(db_session, existing_contract)

            return DAOResponse[ContractResponse](
                success=True, data=ContractResponse.from_orm_model(existing_contract)
            )

        except ValidationError as e:
            return DAOResponse(success=False, validation_error=str(e))
        except Exception as e:
            await db_session.rollback()
            return DAOResponse[ContractResponse](
                success=False, error=f"Fatal Update {str(e)}"
            )

    async def add_contract_details(
        self,
        db_session: AsyncSession,
        contract_id: str,
        contract_info: UnderContractSchema,
        contract: Contract = None,
        under_contract: UnderContract = None,
    ):
        under_contract_dao = BaseDAO(UnderContract)

        try:
            if not isinstance(contract_info, list):
                contract_info = [contract_info]

            for contract_item in contract_info:
                contract_item: UnderContractSchema = contract_item
                # contract_item.contract_status if contract_item.contract_status != contract.contract_status.name else contract.contract_status.name,

                under_contract_obj = {
                    "property_unit_assoc_id": contract_item.property_unit_assoc,
                    "employee_id": contract_item.employee_id,
                    "client_id": contract_item.client_id,
                    "contract_status": contract.contract_status.name,
                    "contract_id": contract_id,
                }

                # Check if the contract info already exists
                if "under_contract_id" in contract_item.model_fields:
                    existing_contract_details: UnderContract = (
                        await under_contract_dao.query(
                            db_session=db_session,
                            filters={
                                "under_contract_id": contract_item.under_contract_id
                            },
                            single=True,
                        )
                    )
                else:
                    existing_contract_details = None

                # create or update contract info
                if existing_contract_details:
                    contract_details = await under_contract_dao.update(
                        db_session=db_session,
                        db_obj=existing_contract_details,
                        obj_in=under_contract_obj.items(),
                    )
                else:
                    contract_details = await under_contract_dao.create(
                        db_session=db_session, obj_in=under_contract_obj
                    )

                # commit object to db session
                await under_contract_dao.commit_and_refresh(
                    db_session, contract_details
                )

            return contract_details
        except ValidationError as e:
            return DAOResponse(success=False, validation_error=str(e))
        except Exception as e:
            return DAOResponse(success=False, error=f"Fatal {str(e)}")
