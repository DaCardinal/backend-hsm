from typing import List
from uuid import UUID
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Amenities, EntityMedia, EntityAmenities
from app.dao.amenities_dao import AmenitiesDAO
from app.schema import AmenitiesSchema
from app.utils import DAOResponse
from app.router.base_router import BaseCRUDRouter

class AmenitiesRouter(BaseCRUDRouter):

    def __init__(self, prefix: str = "", tags: List[str] = []):
        self.dao: AmenitiesDAO = AmenitiesDAO(nesting_degree=BaseCRUDRouter.IMMEDIATE_CHILD, excludes=[''])

        super().__init__(dao=self.dao, schemas=AmenitiesSchema, prefix=prefix,tags = tags)
        self.register_routes()

    def register_routes(self):
        @self.router.post("/link_property_to_ammenity")
        async def add_property_ammenity(property_unit_assoc_id: UUID, ammenity_id: UUID, db: AsyncSession = Depends(self.get_db)):
            property_ammenity : EntityAmenities = await self.dao.link_property_to_ammenity(db_session=db, property_unit_assoc_id=property_unit_assoc_id, ammenity_id=ammenity_id)
            
            if property_ammenity is None:
                raise HTTPException(status_code=404, detail="Error adding ammenity to property")
            
            return DAOResponse(success=True, data=property_ammenity.to_dict())