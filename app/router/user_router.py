from typing import List
from uuid import UUID
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.utils.lifespan import AppLogger
from app.dao.user_dao import UserDAO
from app.schema import UserSchema, UserCreateSchema, UserUpdateSchema
from app.router.base_router import BaseCRUDRouter

class UserRouter(BaseCRUDRouter):

    def __init__(self, dao: UserDAO = UserDAO(User), prefix: str = "", tags: List[str] = []):
        self.dao = dao
        UserSchema["create_schema"] = UserCreateSchema
        UserSchema["update_schema"] = UserUpdateSchema
        super().__init__(dao=dao, schemas=UserSchema, prefix=prefix,tags = tags)
        self.register_routes()

    def register_routes(self):
        @self.router.post("/add_user_role/{user_id}")
        @AppLogger.log_decorator
        async def add_user_role(user_id: UUID, role: str, db: AsyncSession = Depends(self.get_db)):
            user = await self.dao.add_user_role(db_session=db, user_id=user_id, role_alias=role)
            
            if user is None:
                raise HTTPException(status_code=404, detail="User not found")
            return user