from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from uuid import UUID
from sqlalchemy.orm.exc import NoResultFound
from typing import List, Optional, Type, Union

from app.dao.base_dao import BaseDAO
from app.dao.entity_ammenities_dao import EntityAmmenitiesDAO
from app.dao.entity_media_dao import EntityMediaDAO
from app.models import Amenities as AmenitiesModel, EntityAmenities as EntityAmmenities, EntityMedia
from app.schema import AmenitiesBase, Amenities

class AmenitiesDAO(BaseDAO[Amenities]):
    def __init__(self, model: Type[Amenities]):
        super().__init__(model)
        self.primary_key = "amenity_id"
        self.entity_ammenities_dao = EntityAmmenitiesDAO(EntityAmmenities)
        self.enity_media_dao = EntityMediaDAO(EntityMedia)

    async def link_property_to_media(self, db_session: AsyncSession, property_unit_assoc_id: UUID, media_id: UUID, entity_model=None):

        result = await self.enity_media_dao.create(db_session = db_session, obj_in = {
            "entity_type":  entity_model if entity_model else self.model.__name__,
            "media_assoc_id": property_unit_assoc_id,
            "media_id": media_id
        })
        
        return result
    
    async def link_property_to_ammenity(self, db_session: AsyncSession, property_unit_assoc_id: UUID, ammenity_id: UUID, entity_model=None):

        result = await self.entity_ammenities_dao.create(db_session = db_session, obj_in = {
            "property_unit_assoc_id": property_unit_assoc_id,
            "amenity_id": ammenity_id
        })
        
        return result
    
    async def add_entity_ammenity(self, db_session: AsyncSession, entity_id: str, ammenities_info: Union[Amenities | AmenitiesBase | List[Amenities] | List[AmenitiesBase]], entity_model=None, entity_assoc_id=None) -> Optional[Amenities | AmenitiesBase | List[Amenities] | List[AmenitiesBase]]:
        try:
            results = []

            if not isinstance(ammenities_info, list):
                ammenities_info = [ammenities_info]

            for ammenities_item in ammenities_info:
                ammenities_item : Amenities = ammenities_item

                # Check if the address already exists
                existing_ammenities_item = await self.query(db_session=db_session, filters={f"{self.primary_key}": ammenities_item.amenity_id}, single=True, options=[selectinload(Amenities)]) if self.primary_key in ammenities_item.model_fields else None

                if existing_ammenities_item:
                        # Update the existing address
                        obj_data = self.extract_model_data(ammenities_item.model_dump(), Amenities)
                        ammenities_data = Amenities(**obj_data)

                        create_media_item : AmenitiesModel = await self.update(db_session=db_session, db_obj=existing_ammenities_item, obj_in=ammenities_data)

                        await self.entity_ammenities_dao.create(db_session=db_session, obj_in={
                            "property_unit_assoc_id": entity_assoc_id if entity_assoc_id else entity_id,
                            "amenity_id": create_media_item.amenity_id
                        })
                else :
                    create_media_item : Amenities = await self.query(db_session=db_session, filters={**ammenities_item.model_dump()}, single=True)
                    
                    if create_media_item is None:
                        create_media_item : Amenities = await self.create(db_session=db_session, obj_in=ammenities_item.model_dump())

                    await self.entity_ammenities_dao.create(db_session=db_session, obj_in={
                        "property_unit_assoc_id": entity_assoc_id if entity_assoc_id else entity_id,
                        "amenity_id": create_media_item.amenity_id
                    })
                results.append(create_media_item)
            print(f"results {results}")
            return results
        except NoResultFound:
            pass