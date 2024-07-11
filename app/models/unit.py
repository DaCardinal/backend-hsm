from sqlalchemy.orm import relationship
from sqlalchemy import Numeric, Column, ForeignKey, Boolean, Integer, String, Text, UUID

from app.models.property_unit_assoc import PropertyUnitAssoc

# TODO: Review calendar events
class Units(PropertyUnitAssoc):
    __tablename__ = 'units'

    property_unit_assoc_id = Column(UUID(as_uuid=True), ForeignKey('property_unit_assoc.property_unit_assoc_id'), primary_key=True)
    property_unit_code = Column(String(128))
    property_unit_floor_space = Column(Integer)
    property_unit_amount = Column(Numeric(10, 2))
    property_unit_security_deposit = Column(Numeric(10, 2))
    property_unit_commission = Column(Numeric(10, 2))
    property_floor_id = Column(Integer)
    property_unit_notes = Column(Text)
    has_amenities = Column(Boolean, default=False)
    property_id = Column(UUID(as_uuid=True), ForeignKey('property.property_unit_assoc_id'))

    __mapper_args__ = {
        "polymorphic_identity": "Units",
        'inherit_condition': property_unit_assoc_id == PropertyUnitAssoc.property_unit_assoc_id
    }

    maintenance_requests = relationship("MaintenanceRequest",
                                    primaryjoin="Units.property_unit_assoc_id == MaintenanceRequest.property_unit_assoc_id",
                                    foreign_keys="[MaintenanceRequest.property_unit_assoc_id]",
                                    lazy="selectin", back_populates='unit', viewonly=True)
    
    tour_bookings = relationship("Tour",
                                    primaryjoin="Units.property_unit_assoc_id == Tour.property_unit_assoc_id",
                                    foreign_keys="[Tour.property_unit_assoc_id]",
                                    lazy="selectin", back_populates='unit', viewonly=True)
    
    utilities = relationship("EntityBillable",
                            primaryjoin="and_(EntityBillable.entity_assoc_id==Units.property_unit_assoc_id, EntityBillable.entity_type=='Units', EntityBillable.billable_type=='Utilities')",
                            foreign_keys="[EntityBillable.entity_assoc_id]",
                            overlaps="entity_billable,utilities",
                            lazy="selectin", viewonly=True)
    
    # relationship to property
    property = relationship("Property", primaryjoin="Units.property_id == Property.property_unit_assoc_id", back_populates="units", lazy="selectin")

    # relationship with media
    media = relationship("Media",
                         secondary="entity_media",
                         primaryjoin="and_(EntityMedia.media_assoc_id==Units.property_unit_assoc_id, EntityMedia.entity_type=='Units')",
                         overlaps="entity_media,media",
                         lazy="selectin", viewonly=True)
    
    # relationship to link amenities
    entity_amenities = relationship("EntityAmenities",
                                    primaryjoin="Units.property_unit_assoc_id == EntityAmenities.entity_assoc_id",
                                    foreign_keys="[EntityAmenities.entity_assoc_id]",
                                    lazy="selectin", viewonly=True)

    amenities = relationship("Amenities", secondary="entity_amenities",
                             primaryjoin="Units.property_unit_assoc_id == EntityAmenities.entity_assoc_id",
                             secondaryjoin="EntityAmenities.amenity_id == Amenities.amenity_id",
                             lazy="selectin", viewonly=True)
    
    # events = relationship('CalendarEvent',
    #                         secondary="property_unit_assoc", 
    #                         primaryjoin="CalendarEvent.property_unit_assoc_id == PropertyUnitAssoc.property_unit_assoc_id",
    #                         back_populates='unit')