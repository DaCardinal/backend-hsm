from typing import List

from app.models import MaintenanceRequest
from app.dao.maintenance_request_dao import MaintenanceRequestDAO
from app.schema import MaintenanceRequestSchema, MaintenanceRequestCreateSchema, MaintenanceRequestUpdateSchema
from app.router.base_router import BaseCRUDRouter

class MaintenanceRequestRouter(BaseCRUDRouter):

    def __init__(self, dao: MaintenanceRequestDAO = MaintenanceRequestDAO(MaintenanceRequest, load_parent_relationships=False, load_child_relationships=False), prefix: str = "", tags: List[str] = []):
        
        self.dao = dao
        MaintenanceRequestSchema["create_schema"] = MaintenanceRequestCreateSchema
        MaintenanceRequestSchema["update_schema"] = MaintenanceRequestUpdateSchema
        super().__init__(dao=dao, schemas=MaintenanceRequestSchema, prefix=prefix, tags=tags)
        self.register_routes()

    def register_routes(self):
        pass
