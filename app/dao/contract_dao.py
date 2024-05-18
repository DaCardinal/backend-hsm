import uuid
from uuid import UUID
from functools import partial
from pydantic import ValidationError
from typing_extensions import override
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict, List, Type, Optional, Union

from app.dao.base_dao import BaseDAO
from app.dao.contract_type_dao import ContractTypeDAO
from app.dao.payment_type_dao import PaymentTypeDAO
from app.utils import DAOResponse
from app.models import Contract, ContractType, PaymentTypes
from app.schema import ContractCreateSchema, ContractUpdateSchema, ContractResponse, ContractBase

class ContractDAO(BaseDAO[Contract]):
    def __init__(self, model: Type[Contract], load_parent_relationships: bool = False, load_child_relationships: bool = False, excludes = []):
        super().__init__(model, load_parent_relationships, load_child_relationships, excludes=excludes)
        self.primary_key = "contract_id"
        self.contract_type_dao = ContractTypeDAO(ContractType)
        self.payment_type_dao = PaymentTypeDAO(PaymentTypes)

    @override
    async def create(self, db_session: AsyncSession, obj_in: Union[ContractCreateSchema]) -> DAOResponse[ContractResponse]:
        try:
            data = obj_in

            # extract base information
            contract_info : ContractBase = self.extract_model_data(data, ContractBase)

            # check if contract type exists
            existing_contract_type : ContractType = await self.contract_type_dao.query(db_session=db_session, filters={"contract_type_name": contract_info.contract_type}, single=True)

            # if existing_contract_type:
            #     return DAOResponse[ContractResponse](success=False, error="Contract type does not exist", data=ContractResponse.from_orm_model(existing_user))


            return DAOResponse[ContractResponse](success=True, data=ContractResponse.from_orm_model(obj_in))
        except ValidationError as e:
            return DAOResponse(success=False, data=str(e))
        except Exception as e:
            await db_session.rollback()
            return DAOResponse[ContractResponse](success=False, error=f"Fatal {str(e)}")