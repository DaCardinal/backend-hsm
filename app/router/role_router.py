from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.role_dao import RoleDAO
from app.router.base_router import BaseCRUDRouter

# schemas
from app.schema.schemas import RoleSchema
from app.schema.role import RoleUpdateSchema, RoleCreateSchema

class RoleRouter(BaseCRUDRouter):

    def __init__(self, prefix: str = "", tags: List[str] = []):

        # initialize router dao
        RoleSchema["create_schema"] = RoleCreateSchema
        RoleSchema["update_schema"] = RoleUpdateSchema
        self.dao: RoleDAO = RoleDAO(nesting_degree=BaseCRUDRouter.IMMEDIATE_CHILD, excludes=['users'])

        super().__init__(dao=self.dao, schemas=RoleSchema, prefix=prefix,tags = tags)
        self.register_routes()

    def register_routes(self):
        @self.router.post("/add_permission")
        async def add_permission(role_alias: str, permission_alias: str, db: AsyncSession = Depends(self.get_db)):
            role = await self.dao.add_role_permission(db_session=db,  role_alias=role_alias, permission_alias=permission_alias)

            if role is None:
                raise HTTPException(status_code=404, detail="Error adding permission to role.")
            return role
        
        @self.router.get("/stats/")
        async def role_stats(db: AsyncSession = Depends(self.get_db)):
            role = await self.dao.get_role_stats(db_session=db)

            if role is None:
                raise HTTPException(status_code=404, detail="Error retrieving role statistics.")
            return role