import enum
from sqlalchemy.orm import relationship
from sqlalchemy import Numeric, Column, ForeignKey, Boolean, Enum, Integer, String, Text, UUID

from app.models.property_unit_assoc import PropertyUnitAssoc

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

class Property(PropertyUnitAssoc):
    __tablename__ = 'property'

    property_unit_assoc_id = Column(UUID(as_uuid=True), ForeignKey('property_unit_assoc.property_unit_assoc_id'), primary_key=True)
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

    __mapper_args__ = {
        "polymorphic_identity": "Property",
        'inherit_condition': property_unit_assoc_id == PropertyUnitAssoc.property_unit_assoc_id
    }

    maintenance_requests = relationship('MaintenanceRequest',
                                        secondary="property_unit_assoc", 
                                        primaryjoin="MaintenanceRequest.property_unit_assoc_id == PropertyUnitAssoc.property_unit_assoc_id",
                                        overlaps="prop_maintenance_requests",
                                        back_populates='property', viewonly=True)
    
    tour_bookings = relationship('Tour',
                                secondary="property_unit_assoc", 
                                primaryjoin="Tour.property_unit_assoc_id == PropertyUnitAssoc.property_unit_assoc_id",
                                secondaryjoin="PropertyUnitAssoc.property_unit_assoc_id == Property.property_unit_assoc_id",
                                back_populates='property', viewonly=True)
    # events = relationship('CalendarEvent',
    #                         secondary="property_unit_assoc", 
    #                         primaryjoin="CalendarEvent.property_unit_assoc_id == PropertyUnitAssoc.property_unit_assoc_id",
    #                         back_populates='property')
    
    # relationship to units
    units = relationship("Units", primaryjoin="Units.property_id == Property.property_unit_assoc_id", back_populates="property", lazy="selectin")

    # relationship with media
    media = relationship("Media",
                         secondary="entity_media",
                         primaryjoin="and_(EntityMedia.media_assoc_id==Property.property_unit_assoc_id, EntityMedia.entity_type=='Property')",
                         overlaps="entity_media,media",
                         lazy="selectin", viewonly=True)
    
    # relationship to link amenities
    entity_amenities = relationship("EntityAmenities", secondary="property_unit_assoc", viewonly=True, lazy="selectin")

    # relationship to utilities
    utilities = relationship("EntityBillable",
                            primaryjoin="and_(EntityBillable.entity_assoc_id==Property.property_unit_assoc_id, EntityBillable.entity_type=='Property', EntityBillable.billable_type=='Utilities')",
                            foreign_keys="[EntityBillable.entity_assoc_id]",
                            overlaps="entity_billable,utilities",
                            lazy="selectin", viewonly=True)

    amenities = relationship("Amenities", secondary="entity_amenities",
                             primaryjoin="Property.property_unit_assoc_id == EntityAmenities.entity_assoc_id",
                             secondaryjoin="EntityAmenities.amenity_id == Amenities.amenity_id",
                             lazy="selectin", viewonly=True)
    
    # relationship for address
    addresses = relationship(
        'Addresses',
        secondary='entity_address',
        primaryjoin="and_(Property.property_unit_assoc_id==EntityAddress.entity_id, EntityAddress.entity_type=='Property')",
        secondaryjoin="EntityAddress.address_id==Addresses.address_id",
        overlaps="address,entity_addresses,users,properties",
        back_populates="properties",
        lazy="selectin"
    )