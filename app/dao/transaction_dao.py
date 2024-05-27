from uuid import UUID
from typing import Any, List, Type, Union
from typing_extensions import override
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Transaction
from app.dao.base_dao import BaseDAO
from app.utils.response import DAOResponse
from app.schema import TransactionResponse

class TransactionDAO(BaseDAO[Transaction]):
    def __init__(self, model: Type[Transaction], load_parent_relationships: bool = False, load_child_relationships: bool = False, excludes = []):
        super().__init__(model, load_parent_relationships, load_child_relationships, excludes=excludes)
        self.primary_key = "transaction_id"

    @override
    async def get_all(self, db_session: AsyncSession) -> DAOResponse[List[TransactionResponse]]:
        result = await super().get_all(db_session=db_session)
        
        # check if no result
        if not result:
            return DAOResponse(success=True, data=[])

        return DAOResponse[List[TransactionResponse]](success=True, data=[TransactionResponse.from_orm_model(r) for r in result])
    
    @override
    async def get(self, db_session: AsyncSession, id: Union[UUID | Any | int]) -> DAOResponse[TransactionResponse]:
        result : Transaction = await super().get(db_session=db_session, id=id)

        # check if no result
        if not result:
            return DAOResponse(success=True, data={})

        return DAOResponse[TransactionResponse](success=True, data=TransactionResponse.from_orm_model(result))