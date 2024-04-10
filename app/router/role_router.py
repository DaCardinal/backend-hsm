from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Role
from app.dao.user_dao import RoleDAO
from app.schema.user import RoleSchema
from app.router.base_router import BaseCRUDRouter

class RoleRouter(BaseCRUDRouter):

    def __init__(self, dao: RoleDAO = RoleDAO(Role), prefix: str = "", tags: List[str] = []):
        super().__init__(dao=dao, schemas=RoleSchema, prefix=prefix,tags = tags)
        self.dao = dao
        # self.register_routes()

    # def register_routes(self):
    #     @self.router.get("/by-email/{email}", response_model=self.model_schema)
    #     async def read_user_by_email(email: str, db: AsyncSession = Depends(self.get_db)):
    #         user = await self.dao.query(db_session=db, filters={"email": email})
    #         if user is None:
    #             raise HTTPException(status_code=404, detail="User not found")
    #         return user