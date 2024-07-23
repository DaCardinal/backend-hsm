from typing import Optional

from app.dao.resources.base_dao import BaseDAO
from app.models.permissions import Permissions


class PermissionDAO(BaseDAO[Permissions]):
    def __init__(self, excludes=[], nesting_degree: str = BaseDAO.NO_NESTED_CHILD):
        self.model = Permissions
        self.primary_key = "permission_id"

        super().__init__(self.model, nesting_degree=nesting_degree, excludes=excludes)

    async def remove_role(self, role_alias: str) -> Optional[Permissions]:
        pass
