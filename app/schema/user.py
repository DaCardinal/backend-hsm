from enum import Enum
from uuid import UUID
from decimal import Decimal
from datetime import date, datetime
from typing import Any, List, Optional
from pydantic import BaseModel, Field, EmailStr

from app.models import User as UserModel, Addresses,Contract as ContractModel, UnderContract, PropertyUnitAssoc
from app.schema import AddressBase, Address, City, Region, Country, Role

class PropertyStatus(str, Enum):
    available = "available"
    unavailable = "unavailable"

class PropertyType(str, Enum):
    residential = 'residential'
    commercial = 'commercial'
    industrial = 'industrial'

class PropertyBase(BaseModel):
    name: str
    property_type: PropertyType = Field(...)
    amount: float
    security_deposit: Optional[float] = None
    commission: Optional[float] = None
    floor_space: Optional[float] = None
    num_units: Optional[int] = None
    num_bathrooms: Optional[int] = None
    num_garages: Optional[int] = None
    has_balconies: Optional[bool] = False
    has_parking_space: Optional[bool] = False
    pets_allowed: bool = False
    description: Optional[str] = None
    property_status: PropertyStatus = Field(...)

    class Config:
        from_attributes = True
        use_enum_values = True

class Property(PropertyBase):
    property_unit_assoc_id: Optional[UUID]
    address: Optional[List[Address] | Address] = None

    class Config:
        from_attributes = True
        use_enum_values = True
        
class PropertyUnitBase(BaseModel):
    property_unit_code: Optional[str] = None
    property_unit_floor_space: Optional[int] = None
    property_unit_amount: Optional[float] = None
    property_floor_id: Optional[int] = None
    property_unit_notes: Optional[str] = None
    property_unit_security_deposit: Optional[float] = None
    property_unit_commission: Optional[float] = None
    has_amenities: Optional[bool] = False
    property_id: UUID = Field(...)

    class Config:
        from_attributes = True
        use_enum_values = True

class PropertyUnit(PropertyUnitBase):
    property_unit_assoc_id: Optional[UUID]

    class Config:
        from_attributes = True
        use_enum_values = True


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

class ResetPassword(BaseModel):
    email: str
    
class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    other = "other"

class ContractStatus(str, Enum):
    active = "active"
    expired = "expired"
    terminated = "terminated"

class ContractBase(BaseModel):
    property_unit_assoc_id: UUID
    contract_id: UUID
    contract_number: str
    contract_type: str
    payment_type: str
    contract_status: ContractStatus = Field(...)
    contract_details: str
    num_invoices: Optional[Decimal]
    payment_amount: int
    fee_percentage: int
    fee_amount: int
    date_signed: datetime = Field(default_factory=datetime.now)
    start_date: Optional[datetime] = Field(default_factory=datetime.now)
    end_date: Optional[datetime] = Field(default_factory=datetime.now)
    next_payment_due: Optional[datetime] = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True
        use_enum_values = True

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
    address: Optional[AddressBase] = Field(None)
    user_auth_info: Optional[UserAuthCreateInfo] = None
    user_emergency_info: Optional[UserEmergencyInfo] = None
    user_employer_info: Optional[UserEmployerInfo] = None
    role: Optional[str] = None
    
    class Config:
        from_attributes = True

class UserUpdateSchema(UserBase):
    address: Optional[Address] = None
    user_auth_info: Optional[UserAuthInfo] = None
    user_emergency_info: Optional[UserEmergencyInfo] = None
    user_employer_info: Optional[UserEmployerInfo] = None
    role: Optional[str] = None
    
    class Config:
        from_attributes = True

class User(UserBase, UserAuthInfo, UserEmergencyInfo, UserEmployerInfo):
    user_id: Optional[UUID] = None
    addresses: Optional[AddressBase] = None

    class Config:
        from_attributes = True

class Account(BaseModel):
    account_id: UUID
    bank_account_name: str
    bank_account_number: str
    account_branch_name: str

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    user_id: Optional[UUID] = None
    first_name: str = Field(..., max_length=128)
    last_name: str = Field(..., max_length=128)
    email: EmailStr = Field(...)
    phone_number: str = Field(..., max_length=50)
    identification_number: str = Field(..., max_length=80)
    photo_url: str = ""
    gender: GenderEnum = Field(...)
    address: Optional[List[Address] | Address] = None
    user_auth_info: Optional[UserAuthInfo] = None
    user_emergency_info: Optional[UserEmergencyInfo] = None
    user_employer_info: Optional[UserEmployerInfo] = None
    created_at: Optional[datetime] = None
    date_of_birth: Optional[date] = None
    roles: Optional[List[Role]]
    accounts: Optional[List[Account]]
    contracts: Optional[Any] = None
    contracts_count: int = 0
    assigned_properties: Optional[Any] = None
    assigned_properties_count: int = 0

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
    def get_contract_info(cls, contract_info: List[UnderContract]):
        result = []

        for under_contract in contract_info:
            contract: ContractModel = under_contract.contract

            if contract:
                result.append(ContractBase(
                    contract_id = contract.contract_id,
                    num_invoices= Decimal(contract.num_invoices),
                    contract_number = contract.contract_number,
                    contract_type = contract.contract_type_value,
                    payment_type = contract.payment_type_value,
                    contract_status = contract.contract_status,
                    contract_details = contract.contract_details,
                    payment_amount = contract.payment_amount,
                    fee_percentage = contract.fee_percentage,
                    fee_amount = contract.fee_amount,
                    date_signed = contract.date_signed,
                    start_date = contract.start_date,
                    end_date = contract.end_date,
                    property_unit_assoc_id = under_contract.property_unit_assoc_id,
                    next_payment_due = under_contract.next_payment_due
                ))

        return result
    
    @classmethod
    def get_property_info(cls, property: Property):
        property : Property = property

        return Property(
            property_unit_assoc_id = property.property_unit_assoc_id,
            name = property.name,
            property_type = property.property_type.name,
            amount = property.amount,
            security_deposit = property.security_deposit,
            commission = property.commission,
            floor_space = property.floor_space,
            num_units = property.num_units,
            num_bathrooms = property.num_bathrooms,
            num_garages = property.num_garages,
            has_balconies = property.has_balconies,
            has_parking_space = property.has_parking_space,
            pets_allowed = property.pets_allowed,
            description = property.description,
            property_status = property.property_status,
        )
    
    @classmethod
    def get_property_unit_info(cls, property_unit: PropertyUnit):
        property_unit : PropertyUnit = property_unit

        return PropertyUnit(
            property_unit_assoc_id = property_unit.property_unit_assoc_id,
            property_unit_code = property_unit.property_unit_code,
            property_unit_floor_space = property_unit.property_unit_floor_space,
            property_unit_amount = property_unit.property_unit_amount,
            property_floor_id = property_unit.property_floor_id,
            property_unit_notes = property_unit.property_unit_notes,
            has_amenities = property_unit.has_amenities,
            property_id = property_unit.property_id,
            property_unit_security_deposit = property_unit.property_unit_security_deposit,
            property_unit_commission = property_unit.property_unit_commission
        )
    
    @classmethod
    def get_property_details(cls, property_unit_assoc_details: List[PropertyUnitAssoc]):
        result = []

        for property_unit_assoc in property_unit_assoc_details:
            if property_unit_assoc.property_unit_type == "Units":
                property_unit_assoc = cls.get_property_unit_info(property_unit_assoc)
            else:
                property_unit_assoc = cls.get_property_info(property_unit_assoc)

            result.append(property_unit_assoc)
        return result
    
    @classmethod
    def from_orm_model(cls, user: UserModel):
        assigned_properties = cls.get_property_details(user.owned_properties)
        contracts = cls.get_contract_info(user.client_under_contract)


        return cls(
            user_id=user.user_id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            phone_number=user.phone_number,
            identification_number=user.identification_number,
            photo_url=user.photo_url,
            gender=user.gender,
            address=cls.get_address_base(user.addresses),
            user_auth_info=cls.get_user_auth_info(user),
            user_emergency_info=cls.get_user_emergency_info(user),
            user_employer_info=cls.get_user_employer_info(user),
            created_at = user.created_at,
            date_of_birth = user.date_of_birth,
            roles=user.roles,
            accounts = user.accounts,
            contracts = contracts,
            contracts_count = len(contracts),
            assigned_properties = assigned_properties,
            assigned_properties_count = len(assigned_properties)
        ).model_dump()