from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Permissions
from app.dao.permission_dao import PermissionDAO
from app.schema import PermissionSchema
from app.router.base_router import BaseCRUDRouter

class PermissionRouter(BaseCRUDRouter):

    def __init__(self, dao: PermissionDAO = PermissionDAO(Permissions), prefix: str = "", tags: List[str] = []):
        super().__init__(dao=dao, schemas=PermissionSchema, prefix=prefix,tags = tags)
        self.dao = dao
        self.register_routes()

    def register_routes(self):
        @self.router.get("/remove_role/{role_alias}", response_model=self.model_schema)
        async def remove_role(role_alias: str, permission_alias: str, db: AsyncSession = Depends(self.get_db)):
            pass