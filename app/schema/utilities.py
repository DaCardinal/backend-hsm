from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel

class EntityUtilitiesBase(BaseModel):
    utility_id: UUID
    payment_type_id: UUID
    property_unit_assoc_id: UUID
    utility_value: str
    apply_to_units: bool

class EntityUtilitiesCreate(EntityUtilitiesBase):
    pass

class EntityUtilitiesUpdate(EntityUtilitiesBase):
    pass

class EntityUtilities(EntityUtilitiesBase):
    id: UUID

    class Config:
        from_attributes = True

class UtilitiesBase(BaseModel):
    name: str
    description: Optional[str]

    class Config:
        from_attributes = True

class UtilitiesCreateSchema(UtilitiesBase):
    pass

class UtilitiesUpdateSchema(UtilitiesBase):
    pass

class Utilities(UtilitiesBase):
    utility_id: UUID
    utility_value: Optional[str] = None
    apply_to_units: Optional[bool] = None

    class Config:
        from_attributes = True