import enum
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship, selectinload
from sqlalchemy import UUID, Boolean, Column, DateTime, Enum, String, func, select

from app.models.entity_address import EntityAddress
from app.models.address import Addresses
from app.models.model_base import BaseModel as Base
from app.utils.lifespan import get_db as async_session


class GenderEnum(enum.Enum):
    male = "male"
    female = "female"
    other = "other"


# TODO: Review assigned properties
class User(Base):
    __tablename__ = "users"

    user_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4,
    )
    first_name = Column(String(128))
    last_name = Column(String(128))
    email = Column(String(80), unique=True, index=True)
    phone_number = Column(String(50))
    password = Column(String(128))
    identification_number = Column(String(80))
    photo_url = Column(String(128))
    gender = Column(Enum(GenderEnum))
    date_of_birth = Column(String)  # TODO: convert to date_of_birth = Column(Date)

    # Authentication info
    login_provider = Column(String(128), nullable=True, default="native")
    reset_token = Column(String(128), nullable=True)
    verification_token = Column(String(128), nullable=True)
    is_subscribed_token = Column(String(128), nullable=True)
    is_disabled = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=True)
    is_subscribed = Column(Boolean, default=True)
    current_login_time = Column(DateTime(timezone=True), default=func.now())
    last_login_time = Column(DateTime(timezone=True))

    # Employment info
    employer_name = Column(String(128), nullable=True)
    occupation_status = Column(String(128), nullable=True)
    occupation_location = Column(String(128), nullable=True)

    # Emergency Info
    emergency_contact_name = Column(String(128), nullable=True)
    emergency_contact_email = Column(String(128), nullable=True)
    emergency_contact_relation = Column(String(128), nullable=True)
    emergency_contact_number = Column(String(128), nullable=True)
    emergency_address_hash = Column(UUID(as_uuid=True))  # TODO: Change to hash function

    accounts = relationship(
        "Accounts", secondary="user_accounts", back_populates="users", lazy="selectin"
    )
    maintenance_requests = relationship("MaintenanceRequest", back_populates="user")
    tours = relationship("Tour", back_populates="user")
    events = relationship("CalendarEvent", back_populates="organizer")

    addresses = relationship(
        "Addresses",
        secondary="entity_address",
        primaryjoin="and_(User.user_id==EntityAddress.entity_id, EntityAddress.entity_type=='User')",
        secondaryjoin="EntityAddress.address_id==Addresses.address_id",
        overlaps="address,entity_addresses,addresses,properties",
        back_populates="users",
        lazy="selectin",
    )

    roles = relationship(
        "Role", secondary="user_roles", back_populates="users", lazy="selectin"
    )

    sent_messages = relationship("Message", back_populates="sender", lazy="selectin")

    received_messages = relationship(
        "MessageRecipient", back_populates="recipient", lazy="selectin"
    )

    company = relationship(
        "Company", secondary="users_company", back_populates="users", lazy="selectin"
    )

    documents = relationship("Documents", back_populates="users", lazy="selectin")

    interactions_as_user = relationship(
        "UserInteractions",
        foreign_keys="[UserInteractions.user_id]",
        back_populates="user",
        lazy="selectin",
    )
    interactions_as_employee = relationship(
        "UserInteractions",
        foreign_keys="[UserInteractions.employee_id]",
        back_populates="employee",
        lazy="selectin",
    )

    transaction_as_client_offered = relationship(
        "Transaction",
        foreign_keys="[Transaction.client_offered]",
        back_populates="client_offered_transaction",
        lazy="selectin",
    )
    transaction_as_client_requested = relationship(
        "Transaction",
        foreign_keys="[Transaction.client_requested]",
        back_populates="client_requested_transaction",
        lazy="selectin",
    )

    client_under_contract = relationship(
        "UnderContract",
        foreign_keys="[UnderContract.client_id]",
        back_populates="client_representative",
        overlaps="members",
        lazy="selectin",
    )
    employee_under_contract = relationship(
        "UnderContract",
        foreign_keys="[UnderContract.employee_id]",
        back_populates="employee_representative",
        lazy="selectin",
    )

    property = relationship(
        "PropertyUnitAssoc",
        secondary="property_assignment",
        back_populates="assignments",
        lazy="selectin",
    )

    owned_properties = relationship(
        "PropertyUnitAssoc",
        secondary="property_assignment",
        primaryjoin="and_(PropertyAssignment.user_id == User.user_id, PropertyAssignment.assignment_type=='landlord')",
        secondaryjoin="PropertyAssignment.property_unit_assoc_id==PropertyUnitAssoc.property_unit_assoc_id",
        lazy="selectin",
        viewonly=True,
    )

    # assigned_properties = relationship("Property", secondary="property_assignment",
    #                         primaryjoin="and_(PropertyAssignment.user_id == User.user_id, PropertyAssignment.assignment_type=='handler')",
    #                         secondaryjoin="PropertyAssignment.property_unit_assoc_id==Property.property_unit_assoc_id",
    #                         lazy="selectin", viewonly=True)

    # assigned_units = relationship("Units", secondary="property_assignment",
    #                         primaryjoin="and_(PropertyAssignment.user_id == User.user_id, PropertyAssignment.assignment_type=='handler')",
    #                         secondaryjoin="and_(PropertyAssignment.property_unit_assoc_id==Units.property_unit_assoc_id)",
    #                         lazy="selectin", viewonly=True)

    def update_last_login_time(self):
        # Store the current login time in the last_login_time field
        self.last_login_time = self.current_login_time

        # Update the current_login_time field to the current date
        self.current_login_time = datetime.now()

    async def get_user_addresses(self):
        db_session: AsyncSession = async_session()

        async with db_session as session:
            async with session.begin():
                result = await session.execute(
                    select(Addresses)
                    .options(selectinload(Addresses.entity_addresses))
                    .join(
                        EntityAddress, EntityAddress.address_id == Addresses.address_id
                    )
                    .filter(
                        EntityAddress.entity_id == self.user_id,
                        EntityAddress.entity_type == "User",
                    )
                )
                account_addresses = result.scalars().all()
                return account_addresses

    def to_dict(self, exclude=["password"]):
        if exclude is None:
            exclude = set()
        data = {}

        for key in self.__dict__.keys():
            if not key.startswith("_") and key not in exclude:
                value = getattr(self, key)
                if isinstance(value, datetime):
                    value = str(value)
                if isinstance(value, UUID):
                    value = str(value)
                data[key] = value

        return data
