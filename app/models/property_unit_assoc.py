import uuid
import warnings
from sqlalchemy.exc import SAWarning
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, UUID

from app.models.model_base import BaseModel

# Suppress specific SQLAlchemy warnings
warnings.filterwarnings(
    "ignore", 
    category=SAWarning, 
    message=r"^Expression.*is marked as 'remote', but these column\(s\) are local to the local side.*"
)

class PropertyUnitAssoc(BaseModel):
    __tablename__ = 'property_unit_assoc'

    property_unit_assoc_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    property_unit_type = Column(String)

    __mapper_args__ = {
        "polymorphic_on": property_unit_type,         
        "polymorphic_identity": "property_unit_assoc_id"
    }

    members = relationship('User', secondary='under_contract', 
        primaryjoin="and_(PropertyUnitAssoc.property_unit_assoc_id == UnderContract.property_unit_assoc_id)",
        secondaryjoin="and_(UnderContract.client_id == User.user_id)",
        foreign_keys="[UnderContract.property_unit_assoc_id, UnderContract.client_id]", overlaps="client_representative, properties")

    # relationship to assignments
    assignments = relationship('User', secondary='property_assignment', back_populates='property')
    
    # relationship to utilities
    utilities = relationship("Utilities",
                         secondary="entity_utilities",
                         primaryjoin="and_(EntityUtilities.property_unit_assoc_id==PropertyUnitAssoc.property_unit_assoc_id)",
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