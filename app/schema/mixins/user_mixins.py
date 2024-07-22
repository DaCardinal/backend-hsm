from uuid import UUID
from datetime import datetime
from typing import List, Optional, Annotated
from pydantic import BaseModel, ConfigDict, Field, constr, EmailStr

# schemas
from app.schema.enums import GenderEnum

# models
from app.models.user import User as UserModel
from app.models.property_assignment import PropertyAssignment as PropertyAssignmentModel


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

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def get_user_emergency_info(cls, user: UserModel):
        return cls(
            emergency_contact_name=user.emergency_contact_name,
            emergency_contact_email=user.emergency_contact_email,
            emergency_contact_relation=user.emergency_contact_relation,
            emergency_contact_number=user.emergency_contact_number,
            emergency_address_hash=user.emergency_address_hash,
        )


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

    model_config = ConfigDict(__allow_unmapped__=True, from_attributes=True)

    @classmethod
    def get_user_employer_info(cls, user: UserModel):
        return cls(
            employer_name=user.employer_name,
            occupation_status=user.occupation_status,
            occupation_location=user.occupation_location,
        )


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

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def get_user_auth_info(cls, user: UserModel):
        return cls(
            login_provider=user.login_provider,
            reset_token=user.reset_token,
            verification_token=user.verification_token,
            is_subscribed_token=user.is_subscribed_token,
            is_disabled=user.is_disabled,
            is_verified=user.is_verified,
            is_subscribed=user.is_subscribed,
            current_login_time=user.current_login_time,
            last_login_time=user.last_login_time,
        )


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

    model_config = ConfigDict(from_attributes=True)


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

    date_of_birth: Optional[str] = Field(
        None,
        alias="date_of_birth",
        description="The date of birth in YYYY-MM-DD format.",
    )
    first_name: Annotated[str, constr(max_length=128)]
    last_name: Annotated[str, constr(max_length=128)]
    email: EmailStr
    phone_number: Annotated[str, constr(max_length=50)]
    identification_number: Annotated[str, constr(max_length=80)]
    photo_url: Optional[str] = ""
    gender: GenderEnum

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class UserBaseMixin:
    @classmethod
    def get_assigned_users(
        cls, assigned_users: List[PropertyAssignmentModel]
    ) -> List[UserBase]:
        result = []

        for assigned_user in assigned_users:
            user: UserModel = assigned_user.user

            result.append(
                {
                    "user": UserBase(
                        user_id=user.user_id,
                        first_name=user.first_name,
                        last_name=user.last_name,
                        email=user.email,
                        gender=user.gender,
                        phone_number=user.phone_number,
                        photo_url=user.photo_url,
                        identification_number=user.identification_number,
                        date_of_birth=user.date_of_birth,
                    ),
                    "assignment_type": assigned_user.assignment_type,
                }
            )

        return result

    @classmethod
    def get_user_info(cls, user: UserModel):
        """
        Get user information.

        Args:
            user (UserBase): User object.

        Returns:
            UserBase: User object.
        """
        return UserBase(
            user_id=user.user_id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            gender=user.gender,
            phone_number=user.phone_number,
            photo_url=user.photo_url,
            identification_number=user.identification_number,
            date_of_birth=user.date_of_birth,
        )
