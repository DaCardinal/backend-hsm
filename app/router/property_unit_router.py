from typing import List

from app.router.base_router import BaseCRUDRouter
from app.dao.property_unit_dao import PropertyUnitDAO
from app.schema import PropertyUnitSchema, PropertyUnitUpdateSchema, PropertyUnitCreateSchema

class PropertyUnitRouter(BaseCRUDRouter):

    def __init__(self, prefix: str = "", tags: List[str] = []):
        PropertyUnitSchema["create_schema"] = PropertyUnitCreateSchema
        PropertyUnitSchema["update_schema"] = PropertyUnitUpdateSchema
        self.dao: PropertyUnitDAO = PropertyUnitDAO(nesting_degree=BaseCRUDRouter.IMMEDIATE_CHILD, excludes=[''])

        super().__init__(dao=self.dao, schemas=PropertyUnitSchema, prefix=prefix,tags = tags)
        self.register_routes()

    def register_routes(self):
        pass