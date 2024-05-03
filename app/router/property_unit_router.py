from typing import List
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Units as PropertyUnit
from app.dao.property_unit_dao import PropertyUnitDAO
from app.schema import PropertyUnitSchema, PropertyUnitUpdateSchema, PropertyUnitCreateSchema
from app.router.base_router import BaseCRUDRouter

class PropertyUnitRouter(BaseCRUDRouter):

    def __init__(self, dao: PropertyUnitDAO = PropertyUnitDAO(PropertyUnit), prefix: str = "", tags: List[str] = []):
        PropertyUnitSchema["create_schema"] = PropertyUnitCreateSchema
        PropertyUnitSchema["update_schema"] = PropertyUnitUpdateSchema
        super().__init__(dao=dao, schemas=PropertyUnitSchema, prefix=prefix,tags = tags)
        self.dao = dao
        self.register_routes()

    def register_routes(self):
        @self.router.get("/units", response_model=self.model_schema)
        async def property_units(db: AsyncSession = Depends(self.get_db)):
            print("This is a test")
            pass