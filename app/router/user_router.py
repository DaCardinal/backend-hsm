from typing import List, Optional
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.router.base_router import BaseCRUDRouter
from app.dao.user_dao import UserDAO
from app.schema.user import UserSchema
from app.utils.lifespan import get_db, db_manager as database_manager

class UserRouter(BaseCRUDRouter):

    def __init__(self, dao: UserDAO = UserDAO(User), prefix: str = "", tags: List[str] = []):
        super().__init__(
            dao=dao,
            schemas=UserSchema,
            prefix=prefix,
            tags = tags
        )
        self.dao = dao
        self.register_routes()

    def register_routes(self):
        @self.router.get("/by-email/{email}", response_model=self.model_schema)
        async def read_user_by_email(email: str, db: AsyncSession = Depends(self.get_db)):
            user = await self.dao.get_by_email(db_session=db, email=email)
            if user is None:
                raise HTTPException(status_code=404, detail="User not found")
            return user
        
        @self.router.post("/test/")
        async def create_user(user: self.create_schema , db: AsyncSession = Depends(get_db)):
            new_user = User(first_name=user.first_name, last_name=user.last_name, email=user.email)
            created_user = await database_manager.db_module.add_instance(new_user)
            return {"first_name": new_user.first_name, "last_name": new_user.last_name, "email": new_user.email}

        @self.router.get("/test/")
        async def read_users(filter_by_name: Optional[str] = None, db: AsyncSession = Depends(get_db)):

            if filter_by_name is not None:
                users = await database_manager.db_module.get_instances_by_filter(User, first_name=filter_by_name)
            else:
                users = await database_manager.db_module.get_instances(User)
            return users

        @self.router.patch("/test/{user_id}")
        async def update_user(user_id: int, user_updates: self.update_schema, db: AsyncSession = Depends(get_db)):
            updated_user = await database_manager.db_module.update_instance(User, user_id, **user_updates.dict(exclude_unset=True))
            if updated_user is not None:
                return updated_user
            raise HTTPException(status_code=404, detail="User not found")

        @self.router.delete("/tset/{user_id}")
        async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
            deleted_user = await database_manager.db_module.delete_instance(User, user_id)
            if deleted_user is not None:
                return {"detail": "User deleted"}
            raise HTTPException(status_code=404, detail="User not found")


    