from enum import Enum
from uuid import UUID
from datetime import date, datetime
from typing import List, Optional, Union
from pydantic import BaseModel, Field, EmailStr

from app.models import User as UserModel, Addresses
from app.schema import AddressBase, Address, City, Region, Country, Role

class Token(BaseModel):
    access_token: str
    token_type: str

    class Config():
        from_attributes = True

class TokenExposed(BaseModel):
    access_token: str
    token_type: str
    first_name: str
    email: str
    user_id: Optional[UUID] = Field(None)
    last_name: str
    expires: str
    roles : List[Role] = []

    class Config():
        from_attributes = True

class TokenData(BaseModel):
    email: Optional[str] = None

class Login(BaseModel):
    username: str
    password: str
    
class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    other = "other"

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
    login_provider: Optional[str] = Field(None, max_length=128)
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

class UserAuthCreateInfo(BaseModel):
    password: Optional[str] = ""
    login_provider: Optional[str] = Field(..., max_length=128)
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
    user_id: Optional[UUID] = Field(None)
    date_of_birth: Optional[date] = Field(alias='date_of_birth')
    first_name: str = Field(..., max_length=128)
    last_name: str = Field(..., max_length=128)
    email: EmailStr = Field(...)
    phone_number: str = Field(..., max_length=50)
    identification_number: str = Field(..., max_length=80)
    photo_url: Optional[str] = ""
    gender: GenderEnum = Field(...)

    class Config:
        from_attributes = True
        use_enum_values = True

class UserCreateSchema(UserBase):
    address: Optional[AddressBase] = None
    user_auth_info: Optional[UserAuthCreateInfo] = None
    user_emergency_info: Optional[UserEmergencyInfo] = None
    user_employer_info: Optional[UserEmployerInfo] = None
    role: Optional[str] = None
    
    class Config:
        from_attributes = True

class UserUpdateSchema(UserBase):
    address: Optional[Union[AddressBase | Address]] = None
    user_auth_info: Optional[UserAuthInfo] = None
    user_emergency_info: Optional[UserEmergencyInfo] = None
    user_employer_info: Optional[UserEmployerInfo] = None
    
    class Config:
        from_attributes = True

class User(UserBase, UserAuthInfo, UserEmergencyInfo, UserEmployerInfo):
    user_id: Optional[UUID] = None
    addresses: Optional[AddressBase] = None

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    user_id: Optional[UUID] = None
    first_name: str = Field(..., max_length=128)
    last_name: str = Field(..., max_length=128)
    email: EmailStr = Field(...)
    phone_number: str = Field(..., max_length=50)
    # password_hash: str = Field(..., max_length=128)
    identification_number: str = Field(..., max_length=80)
    photo_url: str = ""
    gender: GenderEnum = Field(...)
    roles: Optional[List[Role]]
    address: Optional[List[Address] | Address] = None
    user_auth_info: Optional[UserAuthInfo] = None
    user_emergency_info: Optional[UserEmergencyInfo] = None
    user_employer_info: Optional[UserEmployerInfo] = None
    created_at: Optional[datetime] = None
    date_of_birth: Optional[date] = None

    @classmethod
    def get_address_base(cls, address:List[Addresses]):
        result = []

        for addr in address:
            addr_city : City = addr.city
            addr_region : Region = addr.region
            addr_country : Country = addr.country

            result.append(Address(
                address_id = addr.address_id,
                address_type = addr.address_type,
                primary = addr.primary,
                address_1 = addr.address_1,
                address_2 = addr.address_2,
                address_postalcode = addr.address_postalcode,
                city = addr_city.city_name,
                region = addr_region.region_name,
                country = addr_country.country_name
            ))
        return result

    @classmethod
    def get_user_auth_info(cls, user: User):
        return UserAuthInfo(
            login_provider=user.login_provider,
            reset_token=user.reset_token,
            verification_token=user.verification_token,
            is_subscribed_token=user.is_subscribed_token,
            is_disabled=user.is_disabled,
            is_verified=user.is_verified,
            is_subscribed=user.is_subscribed,
            current_login_time=user.current_login_time,
            last_login_time=user.last_login_time
        )

    @classmethod
    def get_user_emergency_info(cls, user: User):
        return UserEmergencyInfo(
            emergency_contact_name=user.emergency_contact_name,
            emergency_contact_email=user.emergency_contact_email,
            emergency_contact_relation=user.emergency_contact_relation,
            emergency_contact_number=user.emergency_contact_number,
            emergency_address_hash=user.emergency_address_hash
        )

    @classmethod
    def get_user_employer_info(cls, user: User):
        return UserEmployerInfo(
            employer_name=user.employer_name,
            occupation_status=user.occupation_status,
            occupation_location=user.occupation_location
        )

    @classmethod
    def from_orm_model(cls, user: UserModel):

        t = cls(
            user_id=user.user_id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            phone_number=user.phone_number,
            # password_hash=user.password_hash,
            identification_number=user.identification_number,
            photo_url=user.photo_url,
            gender=user.gender,
            roles=user.roles,
            address=cls.get_address_base(user.addresses),
            user_auth_info=cls.get_user_auth_info(user),
            user_emergency_info=cls.get_user_emergency_info(user),
            user_employer_info=cls.get_user_employer_info(user),
            created_at = user.created_at,
            date_of_birth = user.date_of_birth
        ).model_dump()
        return t
