from typing import Type, Optional

from app.dao.base_dao import BaseDAO
from app.models.permissions import Permissions

class PermissionDAO(BaseDAO[Permissions]):
    def __init__(self, model: Type[Permissions]):
        super().__init__(model)
        self.primary_key = "permission_id"

    async def remove_role(self, city_name: str) -> Optional[Permissions]:
        pass