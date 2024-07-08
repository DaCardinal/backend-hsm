from typing import List

from app.schema import PropertyAssignmentSchema
from app.router.base_router import BaseCRUDRouter
from app.dao.property_assignment_dao import PropertyAssignmentDAO

class PropertyAssignmentRouter(BaseCRUDRouter):

    def __init__(self, prefix: str = "", tags: List[str] = []):
        self.dao : PropertyAssignmentDAO = PropertyAssignmentDAO(nesting_degree=BaseCRUDRouter.NO_NESTED_CHILD, excludes=[''])

        super().__init__(dao=self.dao, schemas=PropertyAssignmentSchema, prefix=prefix, tags=tags)
        self.register_routes()

    def register_routes(self):
        pass