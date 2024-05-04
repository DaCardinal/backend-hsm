from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class UnitsAmenitiesBase(BaseModel):
    amenity_id: UUID
    property_unit_assoc_id: UUID
    apply_to_units: bool

class UnitsAmenitiesCreate(UnitsAmenitiesBase):
    pass

class UnitsAmenitiesUpdate(UnitsAmenitiesBase):
    pass

class UnitsAmenities(UnitsAmenitiesBase):
    id: UUID

    class Config:
        from_attributes = True

class AmenitiesBase(BaseModel):
    amenity_name: str
    amenity_short_name: str
    amenity_value_type: str
    description: Optional[str]

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