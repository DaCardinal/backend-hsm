from typing import List

from app.models import Media
from app.dao.media_dao import MediaDAO
from app.schema import MediaSchema
from app.router.base_router import BaseCRUDRouter

class MediaRouter(BaseCRUDRouter):

    def __init__(self, dao: MediaDAO = MediaDAO(Media, load_parent_relationships=False, load_child_relationships=False), prefix: str = "", tags: List[str] = []):
        super().__init__(dao=dao, schemas=MediaSchema, prefix=prefix,tags = tags)
        self.dao = dao
        self.register_routes()

    def register_routes(self):
        pass