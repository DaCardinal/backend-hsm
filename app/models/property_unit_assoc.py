import uuid
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.model_base import BaseModel as Base

class PropertyUnitAssoc(Base):
    __tablename__ = 'property_unit_assoc'
    property_unit_assoc_id = Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True, default=uuid.uuid4)
    property_id = Column(UUID(as_uuid=True), ForeignKey('property.property_id'))
    property_unit_id = Column(UUID(as_uuid=True), ForeignKey('units.property_unit_id'))

    assignments = relationship('User', secondary='property_assignment', back_populates='property')
    
    utilities = relationship("Utilities",
                         secondary="unit_utilities",
                         primaryjoin="and_(UnitUtilities.property_unit_assoc_id==PropertyUnitAssoc.property_unit_assoc_id)",
                         back_populates="units")
    amenities = relationship("Amenities",
                         secondary="units_amenities",
                         primaryjoin="and_(UnitsAmenities.property_unit_assoc_id==PropertyUnitAssoc.property_unit_assoc_id)",
                         overlaps="ammenities",
                         back_populates="units")
    messages_recipients = relationship('MessageRecipient', back_populates='message_group')

    media_ammenities = relationship(
        'Media',
        secondary='entity_media',
        secondaryjoin="and_(PropertyUnitAssoc.property_unit_assoc_id==EntityMedia.entity_id, EntityMedia.entity_type=='Amenities')",
        primaryjoin="EntityMedia.media_id==Media.media_id",
        overlaps="entity_media,media",
        back_populates="properties_units",
        lazy="selectin"
    )
    
    under_contract = relationship('UnderContract', back_populates='properties')