import enum
import uuid
from sqlalchemy.orm import relationship, column_property
from sqlalchemy import Numeric, Column, ForeignKey, Boolean, Enum, Integer, String, Text, UUID,  select

from app.models.model_base import BaseModel as Base
from app.models import PropertyUnitAssoc

class PropertyStatus(enum.Enum):
    available = "available"
    unavailable = "unavailable"
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

    # generate dynamic column property
    property_unit_assoc_id = column_property(
        select(PropertyUnitAssoc.property_unit_assoc_id)
        .where(PropertyUnitAssoc.property_id == property_id)
        .correlate_except(PropertyUnitAssoc)
        .scalar_subquery()
    )

    # relationship to link property unit and generate super key
    property_unit_assoc = relationship("PropertyUnitAssoc", back_populates="property", overlaps="entity_amenities,property")
    
    # relationship to units
    units = relationship("Units", back_populates="property", lazy="selectin")

    # relationship with media
    media = relationship("Media",
                         secondary="entity_media",
                         primaryjoin="and_(EntityMedia.media_assoc_id==Property.property_unit_assoc_id, EntityMedia.entity_type=='Property')",
                         overlaps="entity_media,media",
                         lazy="selectin", viewonly=True)
    
    # relationship to link amenities
    entity_amenities = relationship("EntityAmenities", secondary="property_unit_assoc", viewonly=True)    
    amenities = relationship("Amenities", secondary="entity_amenities",
                             primaryjoin="Property.property_unit_assoc_id == EntityAmenities.property_unit_assoc_id",
                             secondaryjoin="EntityAmenities.amenity_id == Amenities.amenity_id",
                             lazy="selectin", viewonly=True)
    
    # relationship for address
    addresses = relationship(
        'Addresses',
        secondary='entity_address',
        primaryjoin="and_(Property.property_id==EntityAddress.entity_id, EntityAddress.entity_type=='Property')",
        secondaryjoin="EntityAddress.address_id==Addresses.address_id",
        overlaps="address,entity_addresses,users,properties",
        back_populates="properties",
        lazy="selectin"
    )