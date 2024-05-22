from typing import List
from uuid import UUID
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Property, EntityMedia, Amenities
from app.dao.property_dao import PropertyDAO
from app.dao.ammenities_dao import AmenitiesDAO
from app.utils import DAOResponse
from app.schema import PropertySchema, PropertyCreateSchema, PropertyUpdateSchema
from app.router.base_router import BaseCRUDRouter

class PropertyRouter(BaseCRUDRouter):

    def __init__(self, dao: PropertyDAO = PropertyDAO(Property), prefix: str = "", tags: List[str] = []):
        PropertySchema["create_schema"] = PropertyCreateSchema
        PropertySchema["update_schema"] = PropertyUpdateSchema
        self.dao = dao
        super().__init__(dao=dao, schemas=PropertySchema, prefix=prefix,tags = tags)
        self.register_routes()

    def register_routes(self):
        @self.router.post("/link_property_to_media")
        async def add_property_media(property_unit_assoc_id: UUID, media_id: UUID, db: AsyncSession = Depends(self.get_db)):
            media_dao = AmenitiesDAO(Amenities) # Implement this properly
            property_media : EntityMedia = await media_dao.link_property_to_media(db_session=db, property_unit_assoc_id=property_unit_assoc_id, media_id=media_id, entity_model='Property')

            if property_media is None:
                raise HTTPException(status_code=404, detail="Error adding media to property")
            
            return DAOResponse(success=True, data=property_media.to_dict())