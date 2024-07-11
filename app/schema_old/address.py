from enum import Enum
from uuid import UUID
from typing import Any, Optional
import uuid
from pydantic import BaseModel, Field

class City(BaseModel):
    city_id: UUID = Field(default_factory=uuid.uuid4)
    region_id: UUID
    city_name: str = Field(max_length=128)

    class Config:
        from_attributes = True

class Region(BaseModel):
    region_id: UUID = Field(default_factory=uuid.uuid4)
    country_id: UUID
    region_name: str = Field(max_length=128)

    class Config:
        from_attributes = True

class Country(BaseModel):
    country_id: UUID = Field(default_factory=uuid.uuid4)
    country_name: str = Field(max_length=128)

    class Config:
        from_attributes = True

City.model_rebuild()
Region.model_rebuild()

class AddressTypeEnum(str, Enum):
    billing = 'billing'
    mailing = 'mailing'

class AddressBase(BaseModel):
    address_type: AddressTypeEnum
    primary: Optional[bool] = True
    address_1: Optional[str]
    address_2: Optional[str] = None
    city: str|UUID|Any
    region: str|UUID|Any
    country: str|UUID|Any
    address_postalcode: Optional[str]
    
class AddressCreateSchema(AddressBase):

    class Config:
        from_attributes = True

class Address(AddressBase):
    address_id: Optional[UUID] = None

    class Config:
        from_attributes = True

AddressCreateSchema.model_rebuild()

class EntityAddressBase(BaseModel):
    entity_type: str
    entity_id: Optional[str|UUID]
    address_id: str|UUID
    emergency_address: Optional[bool] = False
    emergency_address_hash: Optional[str] = ""

class EntityAddressCreate(EntityAddressBase):

    class Config:
        from_attributes = True

class EntityAddress(EntityAddressBase):
    entity_assoc_id: str|UUID

    class Config:
        from_attributes = True

