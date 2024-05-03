import uuid
from sqlalchemy import Numeric, Column, ForeignKey, Boolean, Enum, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.models.model_base import BaseModel as Base

class PropertyStatus(enum.Enum):
    lease = 'lease'
    sold = 'sold'
    bought = 'bought'
    rent = 'rent'

class PropertyType(enum.Enum):
    residential = 'residential'
    commercial = 'commercial'
    industrial = 'industrial'

class Property(Base):
    __tablename__ = 'property'
    property_id = Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True, default=uuid.uuid4)
    name = Column(String(255))
    address_id = Column(UUID(as_uuid=True), ForeignKey('addresses.address_id'), nullable=True)
    # property_type = Column(UUID(as_uuid=True), ForeignKey('property_type.property_type_id'))
    property_type = Column(Enum(PropertyType))
    amount = Column(Numeric(10, 2))
    security_deposit = Column(Numeric(10, 2))
    commission = Column(Numeric(10, 2))
    floor_space = Column(Numeric(8, 2))
    num_units = Column(Integer)
    num_bathrooms = Column(Integer)
    num_garages = Column(Integer)
    has_balconies = Column(Boolean, default=False)
    has_parking_space = Column(Boolean, default=False)
    pets_allowed = Column(Boolean, default=False)
    description = Column(Text)
    property_status = Column(Enum(PropertyStatus))

    addresses = relationship(
        'Addresses',
        secondary='entity_address',
        primaryjoin="and_(Property.property_id==EntityAddress.entity_id, EntityAddress.entity_type=='Property')",
        secondaryjoin="EntityAddress.address_id==Addresses.address_id",
        overlaps="address,entity_addresses,users,properties",
        back_populates="properties",
        lazy="selectin"
    )
    # property_type = relationship('PropertyType', back_populates='properties')
    units = relationship("Units",
                         secondary="property_unit_assoc",
                         primaryjoin="and_(PropertyUnitAssoc.property_id==Property.property_id)",
                         back_populates="properties", lazy="selectin")