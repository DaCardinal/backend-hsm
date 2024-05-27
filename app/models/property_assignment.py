import enum
from sqlalchemy import Column, ForeignKey, DateTime, Enum, UUID

from app.models.model_base import BaseModel as Base

class AssignmentType(enum.Enum):
    landlord = 'landlord'
    handler = 'handler'
    contractor = 'contractor'
    
class PropertyAssignment(Base):
    __tablename__ = 'property_assignment'
    
    property_assignment_id = Column(UUID(as_uuid=True), primary_key=True)
    property_unit_assoc_id = Column(UUID(as_uuid=True), ForeignKey('property_unit_assoc.property_unit_assoc_id'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'))
    assignment_type = Column(Enum(AssignmentType))
    date_from = Column(DateTime(timezone=True))
    date_to = Column(DateTime(timezone=True))