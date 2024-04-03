from sqlalchemy import create_engine, Column, ForeignKey, Boolean, DateTime, Enum, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from app.models.model_base import BaseModel as Base


class PropertyUnitAssoc(Base):
    __tablename__ = 'property_unit_assoc'
    property_unit_assoc = Column(UUID(as_uuid=True), primary_key=True)
    property_id = Column(UUID(as_uuid=True), ForeignKey('property.property_id'))
    property_unit_id = Column(UUID(as_uuid=True), ForeignKey('units.property_unit_id'))