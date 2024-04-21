from enum import Enum
from uuid import UUID
from datetime import datetime
from typing import Any, Optional
import uuid
from pydantic import BaseModel, Field, EmailStr

from app.models.address import Addresses
from app.schema.base_schema import generate_schemas_for_sqlalchemy_model

AddressSchema = generate_schemas_for_sqlalchemy_model(Addresses, excludes=['address_id'])

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
    description: Optional[str] = None

    class Config:
        from_attributes = True

class Country(BaseModel):
    country_id: UUID = Field(default_factory=uuid.uuid4)
    country_name: str = Field(max_length=128)
    description: Optional[str] = None

    class Config:
        from_attributes = True

City.model_rebuild()
Region.model_rebuild()

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

class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    other = "other"

class AddressTypeEnum(str, Enum):
    billing = 'billing'
    mailing = 'mailing'

class AddressCreateSchema(BaseModel):
    address_type: AddressTypeEnum
    primary: Optional[bool] = True
    address_1: str
    address_2: Optional[str] = None
    city: str|UUID|Any
    region: str|UUID|Any
    country: str|UUID|Any
    address_postalcode: str

    class Config:
        from_attributes = True

class AddressBase(AddressCreateSchema):
    address_id: Optional[str]

AddressCreateSchema.model_rebuild()
class UserEmergencyInfo(BaseModel):
    emergency_contact_name: Optional[str] = Field(None, max_length=128)
    emergency_contact_email: Optional[EmailStr] = Field(...)
    emergency_contact_relation: Optional[str] = Field(None, max_length=128)
    emergency_contact_number: Optional[str] = Field(None, max_length=128)
    emergency_address_hash: Optional[UUID] = None

    class Config:
        from_attributes = True

class UserEmployerInfo(BaseModel):

    employer_name: Optional[str]
    occupation_status: Optional[str]
    occupation_location: Optional[str]

    class Config: 
        __allow_unmapped__ = True
        from_attributes = True

class UserAuthInfo(BaseModel):
    login_provider: str = Field(..., max_length=128)
    reset_token: Optional[str] = Field(None, max_length=128)
    verification_token: Optional[str] = Field(None, max_length=128)
    is_subscribed_token: Optional[str] = Field(None, max_length=128)
    is_disabled: bool = False
    is_verified: bool = True
    is_subscribed: bool = True
    current_login_time: datetime = Field(default_factory=datetime.now)
    last_login_time: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    first_name: str = Field(..., max_length=128)
    last_name: str = Field(..., max_length=128)
    email: EmailStr = Field(...)
    phone_number: str = Field(..., max_length=50)
    password_hash: str = Field(..., max_length=128)
    identification_number: str = Field(..., max_length=80)
    photo_url: str = Field(..., max_length=128)
    gender: GenderEnum = Field(...)

    class Config:
        from_attributes = True
        use_enum_values = True


class User(UserBase, UserAuthInfo, UserEmergencyInfo, UserEmployerInfo):
    user_id: UUID = Field(...)
    addresses: Optional[AddressBase]

    class Config:
        from_attributes = True

class UserCreateSchema(UserBase):
    address: Optional[AddressBase] = None
    user_auth_info: Optional[UserAuthInfo] = None
    user_emergency_info: Optional[UserEmergencyInfo] = None
    user_employer_info: Optional[UserEmployerInfo] = None
    class Config:
        from_attributes = True

class CitySchema(BaseModel):
    city_id: Optional[UUID] = Field(default_factory=UUID, alias='cityId')
    city_name: str = Field(..., alias='cityName')

    class Config:
        from_attributes = True
        populate_by_name = True