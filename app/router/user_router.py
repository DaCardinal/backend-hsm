from uuid import UUID
from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.user_dao import UserDAO
from app.utils.lifespan import AppLogger
from app.router.base_router import BaseCRUDRouter

# schemas
from app.schema.schemas import UserSchema
from app.schema.user import UserCreateSchema, UserUpdateSchema


class UserRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        # initialize router dao
        UserSchema["create_schema"] = UserCreateSchema
        UserSchema["update_schema"] = UserUpdateSchema
        self.dao: UserDAO = UserDAO(
            nesting_degree=BaseCRUDRouter.IMMEDIATE_CHILD, excludes=[""]
        )

        super().__init__(dao=self.dao, schemas=UserSchema, prefix=prefix, tags=tags)
        self.register_routes()

    def register_routes(self):
        @self.router.post("/add_user_role")
        @AppLogger.log_decorator
        async def add_user_role(
            user_id: UUID, role: str, db: AsyncSession = Depends(self.get_db)
        ):
            user = await self.dao.add_user_role(
                db_session=db, user_id=user_id, role_alias=role
            )

            if user is None:
                raise HTTPException(status_code=404, detail="User not found")

            return user

        @self.router.delete("/remove_user_role/")
        async def remove_user_role(
            user_id: UUID, role: str, db: AsyncSession = Depends(self.get_db)
        ):
            user = await self.dao.remove_user_role(
                db_session=db, user_id=user_id, role_alias=role
            )

            if user is None:
                raise HTTPException(status_code=404, detail="User not found")

            return user
