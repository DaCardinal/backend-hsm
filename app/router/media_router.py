from typing import List

from app.models import Media
from app.dao.media_dao import MediaDAO
from app.schema import MediaSchema, MediaCreateSchema, MediaUpdateSchema
from app.router.base_router import BaseCRUDRouter

class MediaRouter(BaseCRUDRouter):

    def __init__(self, prefix: str = "", tags: List[str] = []):
        
        # initialize router dao
        MediaSchema["create_schema"] = MediaCreateSchema
        MediaSchema["update_schema"] = MediaUpdateSchema
        self.dao: MediaDAO = MediaDAO(nesting_degree=BaseCRUDRouter.IMMEDIATE_CHILD, excludes=[''])

        super().__init__(dao=self.dao, schemas=MediaSchema, prefix=prefix,tags = tags)
        self.register_routes()

    def register_routes(self):
        pass