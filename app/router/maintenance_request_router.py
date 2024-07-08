from typing import List

from app.router.base_router import BaseCRUDRouter
from app.dao.maintenance_request_dao import MaintenanceRequestDAO
from app.schema import MaintenanceRequestSchema, MaintenanceRequestCreateSchema, MaintenanceRequestUpdateSchema

class MaintenanceRequestRouter(BaseCRUDRouter):

    def __init__(self, prefix: str = "", tags: List[str] = []):

        MaintenanceRequestSchema["create_schema"] = MaintenanceRequestCreateSchema
        MaintenanceRequestSchema["update_schema"] = MaintenanceRequestUpdateSchema
        self.dao : MaintenanceRequestDAO = MaintenanceRequestDAO(nesting_degree=BaseCRUDRouter.NO_NESTED_CHILD, excludes=[''])

        super().__init__(dao=self.dao, schemas=MaintenanceRequestSchema, prefix=prefix,tags = tags)
        self.register_routes()

    def register_routes(self):
        pass
