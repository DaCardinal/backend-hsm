import enum
import uuid
from sqlalchemy import UUID, Boolean, Column, DateTime, Enum, String, func, select
from sqlalchemy import Column
from sqlalchemy.orm import relationship, selectinload
from sqlalchemy.ext.asyncio import AsyncSession


from app.models.address import Addresses
from app.models.entity_address import EntityAddress
from app.models.model_base import BaseModel as Base
from app.utils.lifespan import get_db as async_session

class GenderEnum(enum.Enum):
    male = 'male'
    female = 'female'
    other = 'other'
    
class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True, default=uuid.uuid4)
    first_name = Column(String(128))
    last_name = Column(String(128))
    email = Column(String(80), unique=True, index=True)
    phone_number = Column(String(50))
    password_hash = Column(String(128))
    identification_number = Column(String(80))
    photo_url = Column(String(128))
    gender = Column(Enum(GenderEnum))

    # # Authentication info
    login_provider = Column(String(128))
    reset_token = Column(String(128))      
    verification_token = Column(String(128))    
    is_subscribed_token = Column(String(128))                   
    is_disabled = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=True)
    is_subscribed = Column(Boolean, default=True)
    current_login_time = Column(DateTime(timezone=True), default=func.now())
    last_login_time = Column(DateTime(timezone=True))
    
    # Employment info
    employer_name = Column(String(128))
    occupation_status = Column(String(128))
    occupation_location = Column(String(128))

    # Emergency Info
    emergency_contact_name = Column(String(128))
    emergency_contact_email = Column(String(128))
    emergency_contact_relation = Column(String(128))
    emergency_contact_number = Column(String(128))
    emergency_address_hash = Column(UUID(as_uuid=True))

    roles = relationship('Role', secondary='user_roles', back_populates='users')
    company = relationship('Company', secondary='users_company', back_populates='users')
    documents = relationship('Documents', back_populates='users')
    sent_messages = relationship('Message', back_populates='sender')
    received_messages = relationship('MessageRecipient', back_populates='receipient')

    interactions_as_user = relationship('UserInteractions',
                                        foreign_keys="[UserInteractions.user_id]",
                                        back_populates='user')
    interactions_as_employee = relationship('UserInteractions',
                                            foreign_keys="[UserInteractions.employee_id]",
                                            back_populates='employee')
    
    transaction_as_client_offered = relationship('Transaction',
                                        foreign_keys="[Transaction.client_offered]",
                                        back_populates='client_offered_transaction')
    transaction_as_client_requested = relationship('Transaction',
                                            foreign_keys="[Transaction.client_requested]",
                                            back_populates='client_requested_transaction')
    
    client_under_contract = relationship('UnderContract',
                                        foreign_keys="[UnderContract.client_id]",
                                        back_populates='client_representative')
    employee_under_contract = relationship('UnderContract',
                                            foreign_keys="[UnderContract.employee_id]",
                                            back_populates='employee_representative')

    property = relationship('PropertyUnitAssoc', secondary='property_assignment', back_populates='assignments')
    
    async def get_user_addresses(self):        
        db_session : AsyncSession = async_session()

        async with db_session as session:
            async with session.begin():

                result = await session.execute(
                    select(Addresses).options(selectinload(Addresses.entity_addresses))
                    .join(EntityAddress, EntityAddress.address_id == Addresses.address_id)
                    .filter(EntityAddress.entity_id == self.user_id, EntityAddress.entity_type == 'user')
                )
                account_addresses = result.scalars().all()
                return account_addresses