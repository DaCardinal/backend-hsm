from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel

from app.schema import Media, MediaBase
from app.models import Media as MediaModel, Amenities as AmenityModel

class EntityAmenitiesBase(BaseModel):
    amenity_id: UUID
    property_unit_assoc_id: UUID
    apply_to_units: bool

class EntityAmenitiesCreate(EntityAmenitiesBase):
    pass

class EntityAmenitiesUpdate(EntityAmenitiesBase):
    pass

class EntityAmenities(EntityAmenitiesBase):
    id: UUID

    class Config:
        from_attributes = True

class AmenitiesBase(BaseModel):
    amenity_name: str
    amenity_short_name: str
    amenity_value_type: str
    description: Optional[str]
    media: Optional[List[Media] | Media] = []

    class Config:
        from_attributes = True
    
    @classmethod
    def get_media(cls, media_items:List[MediaModel]):
        result = []

        for media in media_items:
            # utility_base : Utilities = utility.utility

            # result.append(Utilities(
            #     name = utility_base.name,
            #     description = utility_base.description,
            #     utility_id = utility_base.utility_id,
            #     utility_value = utility.utility_value,
            #     apply_to_units = utility.apply_to_units
            # ))
            pass
        return result
    
    # @classmethod
    # def from_orm_model(cls, amenity: AmenityModel):

    #     return cls(
    #         amenity_name = amenity.amenity_name,
    #         amenity_short_name = amenity.amenity_short_name,
    #         amenity_value_type = amenity.amenity_value_type,
    #         description = amenity.description, 
    #         # media = cls.get_media(amenity)
    #     ).model_dump()

class AmenitiesCreateSchema(BaseModel):
    amenity_name: str
    amenity_short_name: str
    amenity_value_type: str
    description: Optional[str]
    media: Optional[List[MediaBase] | MediaBase] = []

    class Config:
        from_attributes = True

class AmenitiesUpdateSchema(BaseModel):
    amenity_name: str
    amenity_short_name: str
    amenity_value_type: str
    description: Optional[str]

    class Config:
        from_attributes = True


# class AmenitiesUpdateSchema(AmenitiesBase):
#     pass

class Amenities(AmenitiesBase):
    amenity_id: UUID

    class Config:
        from_attributes = True