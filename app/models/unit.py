import uuid
from sqlalchemy import Numeric, Column, ForeignKey, Boolean, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.model_base import BaseModel as Base

class Units(Base):
    __tablename__ = 'units'
    
    property_unit_id = Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True, default=uuid.uuid4)
    # property_unit_type = Column(UUID(as_uuid=True), ForeignKey('unit_type.unit_type_id'))
    property_unit_code = Column(String(128))
    property_unit_floor_space = Column(Integer)
    property_unit_amount = Column(Numeric(10, 2))
    property_floor_id = Column(Integer)
    property_unit_notes = Column(Text)
    has_amenities = Column(Boolean, default=False)

    # unit_type = relationship('UnitType', back_populates='units')
    properties = relationship("Property",
                         secondary="property_unit_assoc",
                         primaryjoin="and_(PropertyUnitAssoc.property_unit_id==Units.property_unit_id)",
                         back_populates="units")
    
    media = relationship("Media",
                         secondary="entity_media",
                         primaryjoin="and_(EntityMedia.entity_id==Units.property_unit_id, EntityMedia.entity_type=='Units')",
                         overlaps="entity_media,media",
                         lazy="selectin")