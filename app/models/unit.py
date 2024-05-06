import uuid
from sqlalchemy import Numeric, Column, ForeignKey, Boolean, Integer, String, Text, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.orm import column_property, foreign

from app.models.model_base import BaseModel as Base
from app.models import PropertyUnitAssoc

class Units(Base):
    __tablename__ = 'units'
    
    property_unit_id = Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True, default=uuid.uuid4)
    property_unit_code = Column(String(128))
    property_unit_floor_space = Column(Integer)
    property_unit_amount = Column(Numeric(10, 2))
    property_floor_id = Column(Integer)
    property_unit_notes = Column(Text)
    has_amenities = Column(Boolean, default=False)
    property_id = Column(UUID(as_uuid=True), ForeignKey('property.property_id'))

    # relationship to link property unit and generate super key
    property_unit_assoc = relationship("PropertyUnitAssoc", back_populates="units", overlaps="entity_amenities,property,units")

    # generate dynamic column property
    property_unit_assoc_id = column_property(
        select(PropertyUnitAssoc.property_unit_assoc_id)
        .where(PropertyUnitAssoc.property_unit_id == property_unit_id, PropertyUnitAssoc.property_id == property_id)
        .correlate_except(PropertyUnitAssoc)
        .scalar_subquery()
    )

    # relationship to property
    property = relationship("Property", back_populates="units", lazy="selectin")

    # relationship with media
    media = relationship("Media",
                         secondary="entity_media",
                         primaryjoin="and_(EntityMedia.media_assoc_id==Units.property_unit_assoc_id, EntityMedia.entity_type=='Units')",
                         overlaps="entity_media,media",
                         lazy="selectin", viewonly=True)
    
    # relationship to link amenities
    entity_amenities = relationship("EntityAmenities", secondary="property_unit_assoc", viewonly=True)    
    amenities = relationship("Amenities", secondary="entity_amenities",
                             primaryjoin="Units.property_unit_assoc_id == EntityAmenities.property_unit_assoc_id",
                             secondaryjoin="EntityAmenities.amenity_id == Amenities.amenity_id",
                             lazy="selectin", viewonly=True)
    
    # unit_type = relationship('UnitType', back_populates='units')
    # properties = relationship("Property",
    #                      secondary="property_unit_assoc",
    #                      primaryjoin="and_(PropertyUnitAssoc.property_unit_id==Units.property_unit_id)",
    #                      back_populates="units")
    
    # media = relationship("Media",
    #                      secondary="entity_media",
    #                      primaryjoin="and_(EntityMedia.media_assoc_id==Units.property_unit_assoc_id, EntityMedia.entity_type=='Units')",
    #                      overlaps="entity_media,media",
    #                      lazy="selectin", viewonly=True)
    
    # ammenities = relationship("EntityAmenities",
    #                     secondary="property_unit_assoc",
    #                     primaryjoin="and_(PropertyUnitAssoc.property_id==Property.property_id, PropertyUnitAssoc.property_unit_id==Units.property_unit_id)",
    #                     overlaps="entity_media,media,ammenities,properties,units",
    #                     lazy="selectin")