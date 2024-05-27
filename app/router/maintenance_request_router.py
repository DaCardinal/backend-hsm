from typing import List

from app.models import MaintenanceRequest
from app.dao.maintenance_request_dao import Maintenance_requestDAO
from app.schema import MaintenanceRequestSchema
from app.router.base_router import BaseCRUDRouter

class MaintenanceRequestRouter(BaseCRUDRouter):

    def __init__(self, dao: Maintenance_requestDAO = Maintenance_requestDAO(MaintenanceRequest, load_parent_relationships=False, load_child_relationships=False), prefix: str = "", tags: List[str] = []):
        super().__init__(dao=dao, schemas=MaintenanceRequestSchema, prefix=prefix, tags=tags)
        self.dao = dao
        self.register_routes()

    def register_routes(self):
        pass
