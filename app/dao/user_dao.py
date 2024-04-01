from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Type, Optional

from app.dao.base_dao import BaseDAO
from app.models.user import UserModel

class UserDAO(BaseDAO[UserModel]):
    def __init__(self, model: Type[UserModel]):
        super().__init__(model)
    
    async def get_by_email(self, db_session: AsyncSession, *, email: str) -> Optional[UserModel]:
        result = await db_session.execute(select(self.model).filter(self.model.email == email))
        return result.scalars().first()