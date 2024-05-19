import uuid
from sqlalchemy import Column, ForeignKey, UUID
from sqlalchemy.orm import relationship

from app.models.model_base import BaseModel as Base

class PropertyUnitAssoc(Base):
    __tablename__ = 'property_unit_assoc'

    property_unit_assoc_id = Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True, default=uuid.uuid4)
    property_id = Column(UUID(as_uuid=True), ForeignKey('property.property_id'))
    property_unit_id = Column(UUID(as_uuid=True), ForeignKey('units.property_unit_id'), default=None)
    
    members = relationship('User', secondary='under_contract', 
        primaryjoin="and_(PropertyUnitAssoc.property_unit_assoc_id == UnderContract.property_unit_assoc_id)",
        secondaryjoin="and_(UnderContract.client_id == User.user_id)",
        foreign_keys="[UnderContract.property_unit_assoc_id, UnderContract.client_id]", overlaps="client_representative, properties")

    # relationship to assignments
    assignments = relationship('User', secondary='property_assignment', back_populates='property')
    
    # relationship to utilities
    utilities = relationship("Utilities",
                         secondary="unit_utilities",
                         primaryjoin="and_(UnitUtilities.property_unit_assoc_id==PropertyUnitAssoc.property_unit_assoc_id)",
                         back_populates="units")
    
    # relationship to amenities
    amenities = relationship("Amenities",
                         secondary="entity_amenities",
                         primaryjoin="and_(EntityAmenities.property_unit_assoc_id==PropertyUnitAssoc.property_unit_assoc_id)",
                         overlaps="ammenities")

    # relationship to message recipients   
    messages_recipients = relationship('MessageRecipient', back_populates='message_group', lazy='selectin')

    # relationship to contracts
    under_contract = relationship('UnderContract', back_populates='properties', overlaps="members", lazy='selectin')

    property = relationship("Property", back_populates="property_unit_assoc", lazy='selectin')
    units = relationship("Units", back_populates="property_unit_assoc", lazy='selectin')