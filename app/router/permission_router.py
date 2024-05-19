from typing import List

from app.models import Permissions
from app.dao.permission_dao import PermissionDAO
from app.schema import PermissionSchema
from app.router.base_router import BaseCRUDRouter

class PermissionRouter(BaseCRUDRouter):

    def __init__(self, dao: PermissionDAO = PermissionDAO(Permissions, load_parent_relationships=True, load_child_relationships=False, excludes=['']), prefix: str = "", tags: List[str] = []):
        self.dao = dao
        super().__init__(dao=dao, schemas=PermissionSchema, prefix=prefix,tags = tags)
        self.register_routes()

    def register_routes(self):
        pass