from typing import Dict
from functools import partial
from pydantic import ValidationError
from typing_extensions import override
from sqlalchemy.ext.asyncio import AsyncSession

# utils
from app.utils.response import DAOResponse

# enums
from app.schema.enums import ContractStatus

# models
from app.models.contract import Contract
from app.models.under_contract import UnderContract

# daos
from app.dao.resources.base_dao import BaseDAO
from app.dao.auth.user_dao import UserDAO
from app.dao.contracts.contract_dao import ContractDAO
from app.dao.properties.property_unit_assoc_dao import PropertyUnitAssocDAO

# schemas
from app.schema.contract import ContractResponse
from app.schema.under_contract import UnderContractCreate


class UnderContractDAO(BaseDAO[UnderContract]):
    def __init__(self, excludes=[], nesting_degree: str = BaseDAO.NO_NESTED_CHILD):
        self.model = UnderContract
        self.primary_key = "under_contract_id"
        self.user_dao = UserDAO()
        self.contract_dao = ContractDAO()
        self.property_unit_assoc_dao = PropertyUnitAssocDAO()

        super().__init__(self.model, nesting_degree=nesting_degree, excludes=excludes)

    @override
    async def create(
        self, db_session: AsyncSession, obj_in: UnderContractCreate
    ) -> DAOResponse[ContractResponse | Dict]:
        try:
            # extract base information
            under_contract_info = self.extract_model_data(
                UnderContractCreate(**obj_in).model_dump(), UnderContractCreate
            )

            client_id = under_contract_info.get("client_id")
            employee_id = under_contract_info.get("employee_id")
            contract_id = under_contract_info.get("contract_id")
            contract_status = under_contract_info.get("contract_status")
            property_unit_assoc = under_contract_info.get("property_unit_assoc")

            # check if contract status exists
            if contract_status not in ContractStatus:
                return DAOResponse(
                    success=False, error="Contract status does not exist", data={}
                )

            # check if client_id and employee_id exists
            client_id_query = await self.user_dao.query(
                db_session=db_session, filters={"user_id": client_id}, single=True
            )

            if not client_id_query:
                return DAOResponse(
                    success=False, error="Client ID does not exist", data={}
                )

            employee_id_query = await self.user_dao.query(
                db_session=db_session, filters={"user_id": employee_id}, single=True
            )

            if not employee_id_query:
                return DAOResponse(
                    success=False, error="Employee ID does not exist", data={}
                )

            # check if contract exists
            contract_id_query: Contract = await self.contract_dao.query(
                db_session=db_session,
                filters={"contract_number": contract_id},
                single=True,
            )

            if not contract_id_query:
                return DAOResponse(
                    success=False, error="Contract ID does not exist", data={}
                )

            # check if property exists
            property_unit_assoc_query = await self.property_unit_assoc_dao.query(
                db_session=db_session,
                filters={"property_unit_assoc_id": property_unit_assoc},
                single=True,
            )

            if not property_unit_assoc_query:
                return DAOResponse(
                    success=False, error="Property ID does not exist", data={}
                )

            details_methods = {
                "contract_info": (
                    partial(
                        self.contract_dao.add_contract_details,
                        contract=contract_id_query,
                    ),
                    UnderContractCreate,
                ),
            }
            contract_info_obj = {"contract_info": obj_in}

            if set(details_methods.keys()).issubset(set(contract_info_obj.keys())):
                t = await self.process_entity_details(
                    db_session,
                    contract_id_query.contract_id,
                    contract_info_obj,
                    details_methods,
                )
                print(t)

            # commit object to db session
            await self.commit_and_refresh(db_session, contract_id_query)

            return DAOResponse[ContractResponse](
                success=True, data=ContractResponse.from_orm_model(contract_id_query)
            )
        except ValidationError as e:
            return DAOResponse(success=False, data=str(e))
        except Exception as e:
            await db_session.rollback()
            return DAOResponse[ContractResponse](success=False, error=f"Fatal {str(e)}")
