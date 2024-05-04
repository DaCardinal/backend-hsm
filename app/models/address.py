import enum
import uuid
from sqlalchemy import UUID, Column, ForeignKey, Boolean, Enum, String
from sqlalchemy.orm import relationship

from app.models.model_base import BaseModel as Base

class AddressTypeEnum(enum.Enum):
    billing = 'billing'
    mailing = 'mailing'

class Addresses(Base):
    __tablename__ = 'addresses'
    address_id = Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True, default=uuid.uuid4)
    address_type = Column(Enum(AddressTypeEnum))
    primary = Column(Boolean, default=True)
    address_1 = Column(String(80))
    address_2 = Column(String(80))
    address_postalcode = Column(String(20))
    city_id = Column(UUID(as_uuid=True), ForeignKey('city.city_id'))
    region_id = Column(UUID(as_uuid=True), ForeignKey('region.region_id'))
    country_id = Column(UUID(as_uuid=True), ForeignKey('country.country_id'))

    users = relationship(
        'User',
        secondary='entity_address',
        primaryjoin="EntityAddress.address_id==Addresses.address_id",
        secondaryjoin="and_(EntityAddress.entity_id==User.user_id, EntityAddress.entity_type=='User')",
        back_populates="addresses",
        lazy="selectin"
    )
    properties = relationship(
        'Property',
        secondary='entity_address',
        primaryjoin="EntityAddress.address_id==Addresses.address_id",
        secondaryjoin="and_(EntityAddress.entity_id==Property.property_id, EntityAddress.entity_type=='Property')",
        back_populates="addresses",
        overlaps="users",
        lazy="selectin"
    )
    
    city = relationship('City', back_populates='addresses', lazy='joined')
    region = relationship('Region', back_populates='addresses', lazy='joined')
    country = relationship('Country', back_populates='addresses', lazy='joined')
    entity_addresses = relationship('EntityAddress', overlaps="users,properties", back_populates='address')