from sqlalchemy import Column, ForeignKey, Boolean, Enum, String
from sqlalchemy.dialects.postgresql import UUID
from app.models.model_base import BaseModel as Base
import enum

class AddressTypeEnum(enum.Enum):
    billing = 'billing'
    mailing = 'mailing'

class Addresses(Base):
    __tablename__ = 'addresses'
    address_id = Column(UUID(as_uuid=True), primary_key=True)
    address_type_id = Column(Enum(AddressTypeEnum))
    primary = Column(Boolean, default=True)
    city_id = Column(UUID(as_uuid=True), ForeignKey('city.city_id'))
    address_1 = Column(String(80))
    address_2 = Column(String(80))
    address_region = Column(String(80))
    address_postalcode = Column(String(20))