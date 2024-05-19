from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Role
from app.dao.role_dao import RoleDAO
from app.schema import RoleSchema
from app.router.base_router import BaseCRUDRouter

class RoleRouter(BaseCRUDRouter):

    def __init__(self, dao: RoleDAO = RoleDAO(Role, load_parent_relationships=True, load_child_relationships=False, excludes=['users']), prefix: str = "", tags: List[str] = []):
        self.dao = dao
        super().__init__(dao=dao, schemas=RoleSchema, prefix=prefix,tags = tags)
        self.register_routes()

    def register_routes(self):
        @self.router.post("/add_permission")
        async def add_permission(role_alias: str, permission_alias: str, db: AsyncSession = Depends(self.get_db)):
            role = await self.dao.add_role_permission(db_session=db,  role_alias=role_alias, permission_alias=permission_alias)

            if role is None:
                raise HTTPException(status_code=404, detail="Error adding permission to role")
            return role