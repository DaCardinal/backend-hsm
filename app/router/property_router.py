from typing import List
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Property
from app.dao.property_dao import PropertyDAO
from app.schema import PropertySchema, PropertyCreateSchema, PropertyUpdateSchema
from app.router.base_router import BaseCRUDRouter

class PropertyRouter(BaseCRUDRouter):

    def __init__(self, dao: PropertyDAO = PropertyDAO(Property), prefix: str = "", tags: List[str] = []):
        PropertySchema["create_schema"] = PropertyCreateSchema
        PropertySchema["update_schema"] = PropertyUpdateSchema
        self.dao = dao
        super().__init__(dao=dao, schemas=PropertySchema, prefix=prefix,tags = tags)
        self.register_routes()

    def register_routes(self):
        pass