from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Media
from app.dao.media_dao import MediaDAO
from app.schema import MediaSchema
from app.router.base_router import BaseCRUDRouter

class MediaRouter(BaseCRUDRouter):

    def __init__(self, dao: MediaDAO = MediaDAO(Media), prefix: str = "", tags: List[str] = []):
        super().__init__(dao=dao, schemas=MediaSchema, prefix=prefix,tags = tags)
        self.dao = dao
        self.register_routes()

    def register_routes(self):
        pass