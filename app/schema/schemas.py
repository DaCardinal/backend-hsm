from enum import Enum
from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr

from app.models.address import Addresses
from app.schema.base_schema import generate_schemas_for_sqlalchemy_model

AddressSchema = generate_schemas_for_sqlalchemy_model(Addresses, excludes=['address_id'])

class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    other = "other"

class UserEmergencyInfo(BaseModel):
    emergency_contact_name: Optional[str] = Field(None, max_length=128)
    emergency_contact_email: Optional[EmailStr] = None
    emergency_contact_relation: Optional[str] = Field(None, max_length=128)
    emergency_contact_number: Optional[str] = Field(None, max_length=128)
    emergency_address_hash: Optional[UUID] = None

    class Config:
        from_attributes = True

class UserEmployerInfo(BaseModel):
    employer_name: Optional[str] = Field(None, max_length=128)
    occupation_status: Optional[str] = Field(None, max_length=128)
    occupation_location: Optional[str] = Field(None, max_length=128)

    class Config: 
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

    class Config:
        from_attributes = True

class UserCreateSchema(UserBase, UserAuthInfo, UserEmergencyInfo, UserEmployerInfo):
    class Config:
        from_attributes = True

class CitySchema(BaseModel):
    city_id: Optional[UUID] = Field(default_factory=UUID, alias='cityId')
    city_name: str = Field(..., alias='cityName')

    class Config:
        from_attributes = True
        populate_by_name = True
        
class AddressTypeEnum(str, Enum):
    billing = 'billing'
    mailing = 'mailing'

class AddressCreateSchema(BaseModel):
    address_type_id: AddressTypeEnum
    primary: Optional[bool] = True
    city_id: Optional[str] = Field(..., alias='city_name')
    city_name: Optional[str]
    address_1: str
    address_2: Optional[str] = None
    address_region: str
    address_postalcode: str

    class Config:
        from_attributes = True

class AddressBase(AddressCreateSchema):
    address_id: Optional[str]

    class Config:
        from_attributes = True
        use_enum_values = True