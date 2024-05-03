import uuid
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.model_base import BaseModel as Base

class PropertyUnitAssoc(Base):
    __tablename__ = 'property_unit_assoc'
    property_unit_assoc = Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True, default=uuid.uuid4)
    property_id = Column(UUID(as_uuid=True), ForeignKey('property.property_id'))
    property_unit_id = Column(UUID(as_uuid=True), ForeignKey('units.property_unit_id'))

    assignments = relationship('User', secondary='property_assignment', back_populates='property')
    
    utilities = relationship("Utilities",
                         secondary="unit_utilities",
                         primaryjoin="and_(UnitUtilities.property_unit_assoc==PropertyUnitAssoc.property_unit_assoc)",
                         back_populates="units")
    amenities = relationship("Amenities",
                         secondary="units_amenities",
                         primaryjoin="and_(UnitsAmenities.property_unit_assoc==PropertyUnitAssoc.property_unit_assoc)",
                         back_populates="units")
    messages_recipients = relationship('MessageRecipient', back_populates='message_group')

    under_contract = relationship('UnderContract', back_populates='properties')