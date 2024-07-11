from uuid import UUID
from decimal import Decimal
from datetime import date, datetime
from pydantic import BaseModel, constr, EmailStr
from typing import Optional, Annotated, List, Any, Union

# schemas
from app.schema.role import Role
from app.schema.account import Account
from app.schema.property import Property, PropertyUnit
from app.schema.enums import GenderEnum, ContractStatus
from app.schema.address import Address, AddressBase, City, Region, Country

# models
from app.models.user import User as UserModel
from app.models.address import Addresses as AddressModel
from app.models.contract import Contract as ContractModel
from app.models.under_contract import UnderContract as UnderContractModel
from app.models.property_unit_assoc import PropertyUnitAssoc as PropertyUnitAssocModel

# models
# UserModel, ContractModel, AddressModel, UnderContractModel
class UserContract(BaseModel):
    """
    Base schema for representing contract information.

    Attributes:
        contract_id (UUID): The unique identifier for the contract.
        contract_type (str): The type of the contract.
        payment_type (str): The type of payment for the contract.
        contract_status (ContractStatus): The status of the contract.
        contract_details (str): The details of the contract.
        num_invoices (int): The number of invoices for the contract.
        payment_amount (int): The payment amount for the contract.
        fee_percentage (int): The fee percentage for the contract.
        fee_amount (int): The fee amount for the contract.
        date_signed (datetime): The date the contract was signed.
        start_date (Optional[datetime]): The start date of the contract.
        end_date (Optional[datetime]): The end date of the contract.
    """
    contract_id: UUID
    contract_type: str
    payment_type: str
    contract_status: ContractStatus
    contract_details: str
    num_invoices: int
    payment_amount: int
    fee_percentage: int
    fee_amount: int
    date_signed: datetime = datetime.now()
    start_date: Optional[datetime] = datetime.now()
    end_date: Optional[datetime] = datetime.now()
    properties: Optional[List[Union[Property, PropertyUnit]]] = None

    class Config:
        from_attributes = True
        use_enum_values = True

class UserEmergencyInfo(BaseModel):
    """
    Model for representing user emergency contact information.

    Attributes:
        emergency_contact_name (Optional[str]): The name of the emergency contact (max length 128).
        emergency_contact_email (Optional[EmailStr]): The email address of the emergency contact.
        emergency_contact_relation (Optional[str]): The relation of the emergency contact to the user (max length 128).
        emergency_contact_number (Optional[str]): The phone number of the emergency contact (max length 128).
        emergency_address_hash (Optional[UUID]): The UUID hash for the emergency address.
    """
    emergency_contact_name: Optional[Annotated[str, constr(max_length=128)]] = None
    emergency_contact_email: Optional[EmailStr] = None
    emergency_contact_relation: Optional[Annotated[str, constr(max_length=128)]] = None
    emergency_contact_number: Optional[Annotated[str, constr(max_length=128)]] = None
    emergency_address_hash: Optional[UUID] = None

    class Config:
        from_attributes = True


class UserEmployerInfo(BaseModel):
    """
    Model for representing user employer information.

    Attributes:
        employer_name (Optional[str]): The name of the employer.
        occupation_status (Optional[str]): The occupation status of the user.
        occupation_location (Optional[str]): The location of the occupation.
    """
    employer_name: Optional[str] = None
    occupation_status: Optional[str] = None
    occupation_location: Optional[str] = None

    class Config:
        __allow_unmapped__ = True  # Allows mapping of unmapped fields
        from_attributes = True


class UserAuthInfo(BaseModel):
    """
    Model for representing user authentication information.

    Attributes:
        login_provider (Optional[str]): The login provider for the user (max length 128).
        reset_token (Optional[str]): The reset token for password resets (max length 128).
        verification_token (Optional[str]): The verification token for account verification (max length 128).
        is_subscribed_token (Optional[str]): The subscription token status (max length 128).
        is_disabled (bool): Indicates if the user account is disabled.
        is_verified (bool): Indicates if the user account is verified.
        is_subscribed (bool): Indicates if the user is subscribed.
        current_login_time (datetime): The current login time of the user.
        last_login_time (Optional[datetime]): The last login time of the user.
    """
    login_provider: Optional[Annotated[str, constr(max_length=128)]] = None
    reset_token: Optional[Annotated[str, constr(max_length=128)]] = None
    verification_token: Optional[Annotated[str, constr(max_length=128)]] = None
    is_subscribed_token: Optional[Annotated[str, constr(max_length=128)]] = None
    is_disabled: bool = False
    is_verified: bool = True
    is_subscribed: bool = True
    current_login_time: datetime = datetime.now()
    last_login_time: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserAuthCreateInfo(BaseModel):
    """
    Model for creating user authentication information.

    Attributes:
        password (Optional[str]): The password for the user account.
        login_provider (Optional[str]): The login provider for the user (max length 128).
        reset_token (Optional[str]): The reset token for password resets (max length 128).
        verification_token (Optional[str]): The verification token for account verification (max length 128).
        is_subscribed_token (Optional[str]): The subscription token status (max length 128).
        is_disabled (bool): Indicates if the user account is disabled.
        is_verified (bool): Indicates if the user account is verified.
        is_subscribed (bool): Indicates if the user is subscribed.
        current_login_time (datetime): The current login time of the user.
        last_login_time (Optional[datetime]): The last login time of the user.
    """
    password: Optional[str] = ""
    login_provider: Optional[Annotated[str, constr(max_length=128)]] = None
    reset_token: Optional[Annotated[str, constr(max_length=128)]] = None
    verification_token: Optional[Annotated[str, constr(max_length=128)]] = None
    is_subscribed_token: Optional[Annotated[str, constr(max_length=128)]] = None
    is_disabled: bool = False
    is_verified: bool = True
    is_subscribed: bool = True
    current_login_time: datetime = datetime.now()
    last_login_time: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    """
    Base model for user information.

    Attributes:
        date_of_birth (Optional[date]): The date of birth of the user.
        first_name (str): The first name of the user (max length 128).
        last_name (str): The last name of the user (max length 128).
        email (EmailStr): The email address of the user.
        phone_number (str): The phone number of the user (max length 50).
        identification_number (str): The identification number of the user (max length 80).
        photo_url (Optional[str]): The URL of the user's photo.
        gender (GenderEnum): The gender of the user.
    """
    date_of_birth: Optional[date] = None
    first_name: Annotated[str, constr(max_length=128)]
    last_name: Annotated[str, constr(max_length=128)]
    email: EmailStr
    phone_number: Annotated[str, constr(max_length=50)]
    identification_number: Annotated[str, constr(max_length=80)]
    photo_url: Optional[str] = ""
    gender: GenderEnum

    class Config:
        from_attributes = True
        use_enum_values = True  # Uses the values of enums instead of their names


class User(UserBase, UserAuthInfo, UserEmergencyInfo, UserEmployerInfo):
    """
    Model for representing a user with detailed information.

    Attributes:
        user_id (Optional[UUID]): The unique identifier for the user.
        addresses (Optional[Any]): The addresses associated with the user.
    """
    user_id: Optional[UUID] = None
    addresses: Optional[AddressBase] = None

    class Config:
        from_attributes = True


class UserCreateSchema(UserBase):
    """
    Schema for creating a new user.

    Attributes:
        address (Optional[AddressBase]): The address of the user.
        user_auth_info (Optional[UserAuthCreateInfo]): The authentication information of the user.
        user_emergency_info (Optional[UserEmergencyInfo]): The emergency contact information of the user.
        user_employer_info (Optional[UserEmployerInfo]): The employer information of the user.
        role (Optional[str]): The role of the user.
    """
    address: Optional[AddressBase] = None
    user_auth_info: Optional[UserAuthCreateInfo] = None
    user_emergency_info: Optional[UserEmergencyInfo] = None
    user_employer_info: Optional[UserEmployerInfo] = None
    role: Optional[str] = None

    class Config:
        from_attributes = True


class UserUpdateSchema(UserBase):
    """
    Schema for updating an existing user.

    Attributes:
        address (Optional[Any]): The address of the user.
        user_auth_info (Optional[UserAuthInfo]): The authentication information of the user.
        user_emergency_info (Optional[UserEmergencyInfo]): The emergency contact information of the user.
        user_employer_info (Optional[UserEmployerInfo]): The employer information of the user.
        role (Optional[str]): The role of the user.
    """
    address: Optional[Address] = None
    user_auth_info: Optional[UserAuthInfo] = None
    user_emergency_info: Optional[UserEmergencyInfo] = None
    user_employer_info: Optional[UserEmployerInfo] = None
    role: Optional[str] = None

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """
    Model for representing a user response.

    Attributes:
        user_id (Optional[UUID]): The unique identifier for the user.
        first_name (str): The first name of the user (max length 128).
        last_name (str): The last name of the user (max length 128).
        email (EmailStr): The email address of the user.
        phone_number (str): The phone number of the user (max length 50).
        identification_number (str): The identification number of the user (max length 80).
        photo_url (str): The URL of the user's photo.
        gender (GenderEnum): The gender of the user.
        address (Optional[List[Address] | Address]): The address(es) of the user.
        user_auth_info (Optional[UserAuthInfo]): The authentication information of the user.
        user_emergency_info (Optional[UserEmergencyInfo]): The emergency contact information of the user.
        user_employer_info (Optional[UserEmployerInfo]): The employer information of the user.
        created_at (Optional[datetime]): The creation time of the user.
        date_of_birth (Optional[date]): The date of birth of the user.
        roles (Optional[List[Role]]): The roles assigned to the user.
        accounts (Optional[List[Account]]): The accounts associated with the user.
        contracts (Optional[Any]): The contracts associated with the user.
        contracts_count (int): The number of contracts associated with the user.
        assigned_properties (Optional[Any]): The properties assigned to the user.
        assigned_properties_count (int): The number of properties assigned to the user.
    """
    user_id: Optional[UUID] = None
    first_name: Annotated[str, constr(max_length=128)]
    last_name: Annotated[str, constr(max_length=128)]
    email: EmailStr
    phone_number: Annotated[str, constr(max_length=50)]
    identification_number: Annotated[str, constr(max_length=80)]
    photo_url: str = ""
    gender: GenderEnum
    address: Optional[List[Address] | Address] = None
    user_auth_info: Optional[UserAuthInfo] = None
    user_emergency_info: Optional[UserEmergencyInfo] = None
    user_employer_info: Optional[UserEmployerInfo] = None
    created_at: Optional[datetime] = datetime.now()
    date_of_birth: Optional[date] = None
    roles: Optional[List[Role]] = None
    accounts: Optional[List[Account]] = None
    contracts: Optional[Any] = None # TODO: Add actual contract information
    contracts_count: int = 0
    assigned_properties: Optional[Any] = None
    assigned_properties_count: int = 0

    @classmethod
    def get_address_base(cls, address: List[AddressModel]):
        """
        Get base address information.

        Args:
            address (List[Address]): List of addresses.

        Returns:
            List[Address]: List of address objects.
        """
        result = []
        
        for addr in address:
            addr_city: City = addr.city
            addr_region: Region = addr.region
            addr_country: Country = addr.country

            result.append(Address(
                address_id=addr.address_id,
                address_type=addr.address_type,
                primary=addr.primary,
                address_1=addr.address_1,
                address_2=addr.address_2,
                address_postalcode=addr.address_postalcode,
                city=addr_city.city_name,
                region=addr_region.region_name,
                country=addr_country.country_name
            ))

        return result

    @classmethod
    def get_user_auth_info(cls, user: User):
        """
        Get user authentication information.

        Args:
            user (User): User object.

        Returns:
            UserAuthInfo: User authentication information.
        """
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
        """
        Get user emergency information.

        Args:
            user (User): User object.

        Returns:
            UserEmergencyInfo: User emergency contact information.
        """
        return UserEmergencyInfo(
            emergency_contact_name=user.emergency_contact_name,
            emergency_contact_email=user.emergency_contact_email,
            emergency_contact_relation=user.emergency_contact_relation,
            emergency_contact_number=user.emergency_contact_number,
            emergency_address_hash=user.emergency_address_hash
        )

    @classmethod
    def get_user_employer_info(cls, user: User):
        """
        Get user employer information.

        Args:
            user (User): User object.

        Returns:
            UserEmployerInfo: User employer information.
        """
        return UserEmployerInfo(
            employer_name=user.employer_name,
            occupation_status=user.occupation_status,
            occupation_location=user.occupation_location
        )

    @classmethod
    def get_contract_info(cls, contract_info: List[UnderContractModel]):
        """
        Get contract information.

        Args:
            contract_info (List[UnderContract]): List of contract information.

        Returns:
            List[ContractBase]: List of contract base objects.
        """
        result = []

        for under_contract in contract_info:
            contract: ContractModel = under_contract.contract

            if contract:
                result.append(UserContract(
                    contract_id=contract.contract_id,
                    num_invoices=Decimal(contract.num_invoices),
                    contract_number=contract.contract_number,
                    contract_type=contract.contract_type_value,
                    payment_type=contract.payment_type_value,
                    contract_status=contract.contract_status,
                    contract_details=contract.contract_details,
                    payment_amount=contract.payment_amount,
                    fee_percentage=contract.fee_percentage,
                    fee_amount=contract.fee_amount,
                    date_signed=contract.date_signed,
                    start_date=contract.start_date,
                    end_date=contract.end_date,
                    property_unit_assoc_id=under_contract.property_unit_assoc_id,
                    next_payment_due=under_contract.next_payment_due,
                    properties=contract.properties
                ))
        return result

    @classmethod
    def get_property_info(cls, property: Property):
        """
        Get property information.

        Args:
            property (Property): Property object.

        Returns:
            Property: Property object.
        """
        return Property(
            property_unit_assoc_id=property.property_unit_assoc_id,
            name=property.name,
            property_type=property.property_type.name,
            amount=property.amount,
            security_deposit=property.security_deposit,
            commission=property.commission,
            floor_space=property.floor_space,
            num_units=property.num_units,
            num_bathrooms=property.num_bathrooms,
            num_garages=property.num_garages,
            has_balconies=property.has_balconies,
            has_parking_space=property.has_parking_space,
            pets_allowed=property.pets_allowed,
            description=property.description,
            property_status=property.property_status
        )

    @classmethod
    def get_property_unit_info(cls, property_unit: PropertyUnit):
        """
        Get property unit information.

        Args:
            property_unit (PropertyUnit): Property unit object.

        Returns:
            PropertyUnit: Property unit object.
        """
        return PropertyUnit(
            property_unit_assoc_id=property_unit.property_unit_assoc_id,
            property_unit_code=property_unit.property_unit_code,
            property_unit_floor_space=property_unit.property_unit_floor_space,
            property_unit_amount=property_unit.property_unit_amount,
            property_floor_id=property_unit.property_floor_id,
            property_unit_notes=property_unit.property_unit_notes,
            has_amenities=property_unit.has_amenities,
            property_id=property_unit.property_id,
            property_unit_security_deposit=property_unit.property_unit_security_deposit,
            property_unit_commission=property_unit.property_unit_commission
        )

    @classmethod
    def get_property_details(cls, property_unit_assoc_details: List[PropertyUnitAssocModel]):
        """
        Get property details.

        Args:
            property_unit_assoc_details (List[PropertyUnitAssoc]): List of property unit associations.

        Returns:
            List[PropertyUnitAssoc]: List of property unit association objects.
        """
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
        """
        Create a UserResponse instance from an ORM model.

        Args:
            user (UserModel): User ORM model.

        Returns:
            UserResponse: User response object.
        """
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
            created_at=user.created_at,
            date_of_birth=user.date_of_birth,
            roles=user.roles,
            accounts=user.accounts,
            contracts=contracts,
            contracts_count=len(contracts),
            assigned_properties=assigned_properties,
            assigned_properties_count=len(assigned_properties)
        ).model_dump()