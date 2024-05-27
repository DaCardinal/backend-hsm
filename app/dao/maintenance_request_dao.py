from typing import Type

from app.dao.base_dao import BaseDAO
from app.models import MaintenanceRequest

class Maintenance_requestDAO(BaseDAO[MaintenanceRequest]):
    def __init__(self, model: Type[MaintenanceRequest], load_parent_relationships: bool = False, load_child_relationships: bool = False, excludes = []):
        super().__init__(model, load_parent_relationships, load_child_relationships, excludes=excludes)
        self.primary_key = "task_number"
