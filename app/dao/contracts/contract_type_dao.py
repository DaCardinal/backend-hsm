from typing import Optional
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

# dao
from app.dao.resources.base_dao import BaseDAO

# models
from app.models.contract_type import ContractType


class ContractTypeDAO(BaseDAO[ContractType]):
    def __init__(self, excludes=[], nesting_degree: str = BaseDAO.NO_NESTED_CHILD):
        self.model = ContractType
        self.primary_key = "contract_type_id"

        super().__init__(self.model, nesting_degree=nesting_degree, excludes=excludes)

    async def get_existing_contract_type(
        self, db_session: AsyncSession, contract_type: str
    ) -> Optional[ContractType]:
        payment_type_result = await self.query(
            db_session=db_session,
            filters={"contract_type_name": contract_type},
            single=True,
        )

        if not payment_type_result:
            raise NoResultFound("Contract type does not exist")

        return payment_type_result
