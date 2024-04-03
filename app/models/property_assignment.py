from sqlalchemy import create_engine, Column, ForeignKey, Boolean, DateTime, Enum, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from app.models.model_base import BaseModel as Base

class PropertyAssignment(Base):
    __tablename__ = 'property_assignment'
    property_assignment_id = Column(UUID(as_uuid=True), primary_key=True)
    property_id = Column(UUID(as_uuid=True), ForeignKey('property.property_id'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'))
    date_from = Column(DateTime)
    date_to = Column(DateTime)