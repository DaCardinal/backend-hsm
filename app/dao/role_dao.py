from typing import Type, Optional

from app.dao.base_dao import BaseDAO
from app.models.role import Role

class RoleDAO(BaseDAO[Role]):
    def __init__(self, model: Type[Role]):
        super().__init__(model)

    async def add_user(self, user_id: str, role_id: str) -> Optional[Role]:
        pass