from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel
from app.schema import Media

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
    media: Optional[List[Media] | Media] 

    class Config:
        from_attributes = True

class AmenitiesCreateSchema(AmenitiesBase):
    pass

class AmenitiesUpdateSchema(AmenitiesBase):
    pass

class Amenities(AmenitiesBase):
    amenity_id: UUID

    class Config:
        from_attributes = True