from sqlalchemy import Numeric, create_engine, Column, ForeignKey, Boolean, DateTime, Enum, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from app.models.model_base import BaseModel as Base
import enum

class UnitUtilities(Base):
    __tablename__ = 'unit_utilities'
    id = Column(UUID(as_uuid=True), primary_key=True)
    utility_id = Column(UUID(as_uuid=True), ForeignKey('utilities.utility_id'))
    payment_type_id = Column(UUID(as_uuid=True), ForeignKey('payment_types.payment_type_id'))
    property_unit_assoc = Column(UUID(as_uuid=True), ForeignKey('property_unit_assoc.property_unit_assoc'))
    utility_value = Column(String(128))
    apply_to_units = Column(Boolean, default=False)
