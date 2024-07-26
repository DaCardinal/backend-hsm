import asyncio
from uuid import UUID
from pydantic import ValidationError
from typing_extensions import override
from typing import Dict, Union
from sqlalchemy.ext.asyncio import AsyncSession

# utils
from app.utils.response import DAOResponse

# enums
from app.schema.enums import ContractStatus

# models
from app.models.under_contract import UnderContract

# daos
from app.dao.resources.base_dao import BaseDAO
from app.dao.auth.user_dao import UserDAO
from app.dao.contracts.contract_dao import ContractDAO
from app.dao.properties.property_unit_assoc_dao import PropertyUnitAssocDAO

# schemas
from app.schema.under_contract import (
    UnderContractCreate,
    UnderContractUpdate,
    UnderContractResponse,
)


class UnderContractDAO(BaseDAO[UnderContract]):
    def __init__(self, excludes=[], nesting_degree: str = BaseDAO.NO_NESTED_CHILD):
        super().__init__(
            UnderContract, nesting_degree=nesting_degree, excludes=excludes
        )
        self.primary_key = "under_contract_id"
        self.user_dao = UserDAO()
        self.contract_dao = ContractDAO()
        self.property_unit_assoc_dao = PropertyUnitAssocDAO()

    async def _validate_ids(
        self,
        db_session: AsyncSession,
        client_id: UUID,
        employee_id: UUID,
        contract_id: str,
        property_unit_assoc: UUID,
    ) -> Union[None, DAOResponse]:
        user_dao_queries = [
            self.user_dao.query(
                db_session, filters={"user_id": client_id}, single=True
            ),
            self.user_dao.query(
                db_session, filters={"user_id": employee_id}, single=True
            ),
        ]
        contract_dao_query = self.contract_dao.query(
            db_session, filters={"contract_number": contract_id}, single=True
        )
        property_unit_assoc_dao_query = self.property_unit_assoc_dao.query(
            db_session,
            filters={"property_unit_assoc_id": property_unit_assoc},
            single=True,
        )

        client, employee, contract, property_unit = await asyncio.gather(
            *user_dao_queries, contract_dao_query, property_unit_assoc_dao_query
        )

        if not client:
            return DAOResponse(success=False, error="Client ID does not exist", data={})
        if not employee:
            return DAOResponse(
                success=False, error="Employee ID does not exist", data={}
            )
        if not contract:
            return DAOResponse(
                success=False, error="Contract ID does not exist", data={}
            )
        if not property_unit:
            return DAOResponse(
                success=False, error="Property ID does not exist", data={}
            )

    @override
    async def create(
        self, db_session: AsyncSession, obj_in: UnderContractCreate
    ) -> DAOResponse[UnderContractResponse | Dict]:
        try:
            under_contract_info = UnderContractCreate(**obj_in).model_dump()
            validation_response = await self._validate_ids(
                db_session,
                under_contract_info.get("client_id"),
                under_contract_info.get("employee_id"),
                under_contract_info.get("contract_id"),
                under_contract_info.get("property_unit_assoc_id"),
            )
            if validation_response:
                return validation_response

            if under_contract_info.get("contract_status") not in ContractStatus:
                return DAOResponse(
                    success=False, error="Contract status does not exist", data={}
                )

            contract_assignment = await super().create(
                db_session, obj_in=under_contract_info
            )
            await self.commit_and_refresh(db_session, contract_assignment)

            return DAOResponse[UnderContractResponse](
                success=True,
                data=UnderContractResponse.from_orm_model(contract_assignment),
            )
        except ValidationError as e:
            return DAOResponse(success=False, data=str(e))
        except Exception as e:
            await db_session.rollback()
            return DAOResponse[UnderContractResponse](
                success=False, error=f"Fatal {str(e)}"
            )

    @override
    async def update(
        self,
        db_session: AsyncSession,
        db_obj: UnderContract,
        obj_in: UnderContractUpdate,
    ) -> DAOResponse[UnderContractResponse | Dict]:
        try:
            under_contract_info = obj_in.model_dump()
            validation_response = await self._validate_ids(
                db_session,
                under_contract_info.get("client_id"),
                under_contract_info.get("employee_id"),
                under_contract_info.get("contract_id"),
                under_contract_info.get("property_unit_assoc_id"),
            )
            if validation_response:
                return validation_response

            if under_contract_info.get("contract_status") not in ContractStatus:
                return DAOResponse(
                    success=False, error="Contract status does not exist", data={}
                )

            contract_assignment_data = obj_in.model_dump(
                exclude=[
                    "under_contract_id",
                    "properties",
                    "contract",
                    "client_representative",
                    "employee_representative",
                ]
            )

            contract_assignment = await super().update(
                db_session=db_session,
                db_obj=db_obj,
                obj_in=list(contract_assignment_data.items()),
            )
            await self.commit_and_refresh(db_session, contract_assignment)

            return DAOResponse[UnderContractResponse](
                success=True,
                data=UnderContractResponse.from_orm_model(contract_assignment),
            )
        except ValidationError as e:
            return DAOResponse(success=False, data=str(e))
        except Exception as e:
            await db_session.rollback()
            return DAOResponse[UnderContractResponse](
                success=False, error=f"Fatal {str(e)}"
            )
