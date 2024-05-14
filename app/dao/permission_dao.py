from typing import Type, Optional

from app.dao.base_dao import BaseDAO
from app.models.permissions import Permissions

class PermissionDAO(BaseDAO[Permissions]):
    def __init__(self, model: Type[Permissions], load_parent_relationships: bool = False, load_child_relationships: bool = False, excludes = []):
        super().__init__(model, load_parent_relationships, load_child_relationships, excludes=excludes)
        self.primary_key = "permission_id"

    async def remove_role(self, city_name: str) -> Optional[Permissions]:
        pass