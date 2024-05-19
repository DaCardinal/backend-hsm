from typing import List
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Units as PropertyUnit
from app.dao.property_unit_dao import PropertyUnitDAO
from app.schema import PropertyUnitSchema, PropertyUnitUpdateSchema, PropertyUnitCreateSchema
from app.router.base_router import BaseCRUDRouter

class PropertyUnitRouter(BaseCRUDRouter):

    def __init__(self, dao: PropertyUnitDAO = PropertyUnitDAO(PropertyUnit, load_parent_relationships=True, load_child_relationships=False), prefix: str = "", tags: List[str] = []):
        self.dao = dao
        PropertyUnitSchema["create_schema"] = PropertyUnitCreateSchema
        PropertyUnitSchema["update_schema"] = PropertyUnitUpdateSchema
        super().__init__(dao=dao, schemas=PropertyUnitSchema, prefix=prefix,tags = tags)
        self.register_routes()

    def register_routes(self):
        pass