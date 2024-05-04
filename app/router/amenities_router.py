from typing import List
from uuid import UUID
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Amenities
from app.dao.ammenities_dao import AmenitiesDAO
from app.schema import AmmenitiesSchema
from app.router.base_router import BaseCRUDRouter

class AmmenitiesRouter(BaseCRUDRouter):

    def __init__(self, dao: AmenitiesDAO = AmenitiesDAO(Amenities), prefix: str = "", tags: List[str] = []):
        super().__init__(dao=dao, schemas=AmmenitiesSchema, prefix=prefix,tags = tags)
        self.dao = dao
        self.register_routes()

    def register_routes(self):
        @self.router.post("/link_property_to_media")
        async def add_property_media(property_unit_assoc_id: UUID, media_id: UUID, db: AsyncSession = Depends(self.get_db)):
            property_media = await self.dao.link_property_to_media(db_session=db, property_unit_assoc_id=property_unit_assoc_id, media_id=media_id)

            if property_media is None:
                raise HTTPException(status_code=404, detail="Error adding media to property")
            return property_media