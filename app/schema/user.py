from uuid import UUID
from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, constr, EmailStr
from typing import Optional, Annotated, List, Any, Union

# models
from app.models.user import User as UserModel

# schemas
from app.schema.role import Role
from app.schema.account import Account
from app.schema.enums import GenderEnum, ContractStatus

# mixins
from app.schema.mixins.contract_mixin import ContractInfoMixin
from app.schema.mixins.property_mixin import Property, PropertyUnit
from app.schema.mixins.address_mixin import AddressMixin, Address, AddressBase
from app.schema.mixins.user_mixins import (
    UserBase,
    UserAuthInfo,
    UserAuthCreateInfo,
    UserEmergencyInfo,
    UserEmployerInfo,
)


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

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class User(UserBase, UserAuthInfo, UserEmergencyInfo, UserEmployerInfo):
    """
    Model for representing a user with detailed information.

    Attributes:
        user_id (Optional[UUID]): The unique identifier for the user.
        addresses (Optional[Any]): The addresses associated with the user.
    """

    user_id: Optional[UUID] = None
    addresses: Optional[AddressBase] = None

    model_config = ConfigDict(from_attributes=True)


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

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={date: lambda v: v.strftime("%Y-%m-%d") if v else None},
    )


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

    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel, ContractInfoMixin):
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
    contracts: Optional[List[UserContract]] = None
    contracts_count: int = 0
    assigned_properties: Optional[Any] = None
    assigned_properties_count: int = 0

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
            address=AddressMixin.get_address_base(user.addresses),
            user_auth_info=UserAuthInfo.get_user_auth_info(user),
            user_emergency_info=UserEmergencyInfo.get_user_emergency_info(user),
            user_employer_info=UserEmployerInfo.get_user_employer_info(user),
            created_at=user.created_at,
            date_of_birth=user.date_of_birth,
            roles=user.roles,
            accounts=user.accounts,
            contracts=contracts,
            contracts_count=len(contracts),
            assigned_properties=assigned_properties,
            assigned_properties_count=len(assigned_properties),
        ).model_dump()
