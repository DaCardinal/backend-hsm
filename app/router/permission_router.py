from typing import List

from app.dao.permission_dao import PermissionDAO
from app.router.base_router import BaseCRUDRouter

# schemas
from app.schema.schemas import PermissionSchema

class PermissionRouter(BaseCRUDRouter):

    def __init__(self, prefix: str = "", tags: List[str] = []):
        self.dao: PermissionDAO = PermissionDAO(nesting_degree=BaseCRUDRouter.IMMEDIATE_CHILD, excludes=[''])

        super().__init__(dao=self.dao, schemas=PermissionSchema, prefix=prefix,tags = tags)
        self.register_routes()

    def register_routes(self):
        pass