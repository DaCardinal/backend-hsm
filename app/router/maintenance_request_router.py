from typing import List

from app.router.base_router import BaseCRUDRouter

# daos
from app.dao.communication.maintenance_request_dao import MaintenanceRequestDAO

# schemas
from app.schema.schemas import MaintenanceRequestSchema
from app.schema.maintenance_request import (
    MaintenanceRequestCreateSchema,
    MaintenanceRequestUpdateSchema,
)


class MaintenanceRequestRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        MaintenanceRequestSchema["create_schema"] = MaintenanceRequestCreateSchema
        MaintenanceRequestSchema["update_schema"] = MaintenanceRequestUpdateSchema
        self.dao: MaintenanceRequestDAO = MaintenanceRequestDAO(
            nesting_degree=BaseCRUDRouter.NO_NESTED_CHILD, excludes=[""]
        )

        super().__init__(
            dao=self.dao, schemas=MaintenanceRequestSchema, prefix=prefix, tags=tags
        )
        self.register_routes()

    def register_routes(self):
        pass
