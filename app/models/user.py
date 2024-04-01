import enum
from sqlalchemy import TIMESTAMP, UUID, Enum, Boolean, Column, Integer, String

from app.models.model_base import BaseModel

class GenderEnum(enum.Enum):
    male = 'male'
    female = 'female'
    other = 'other'
    
class UserModel(BaseModel):
    __tablename__ = "users"

    # user_id = Column(UUID(as_uuid=True), primary_key=True)
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(128))
    last_name = Column(String(128))
    email = Column(String(80), unique=True, index=True)
    # phone_number = Column(String(50))
    # password_hash = Column(String(128))
    # identification_number = Column(String(80))
    # photo_url = Column(String(128))
    # gender = Column(Enum(GenderEnum))

    # # Authentication info
    # reset_token = Column(String(128))      
    # verification_token = Column(String(128))    
    # is_subscribed_token = Column(String(128))                   
    # is_disabled = Column(Boolean, default=False)
    # is_verified = Column(Boolean, default=True)
    # is_subscribed = Column(Boolean, default=True)
    # login_provider = Column(String(128))
    # current_login_time = Column(TIMESTAMP)
    # last_login_time = Column(TIMESTAMP)

    # # Employment info
    # employer_name = Column(String(128))
    # occupation_status = Column(String(128))
    # occupation_location = Column(String(128))

    # # Emergency Info
    # emergency_contact_name = Column(String(128))
    # emergency_contact_email = Column(String(128))
    # emergency_contact_relation = Column(String(128))
    # emergency_contact_number = Column(String(128))
    # emergency_address_hash = Column(UUID(as_uuid=True))