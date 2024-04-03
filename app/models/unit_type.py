from sqlalchemy import Numeric, create_engine, Column, ForeignKey, Boolean, DateTime, Enum, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from app.models.model_base import BaseModel as Base
import enum

class UnitType(Base):
    __tablename__ = 'unit_type'
    unit_type_id = Column(UUID(as_uuid=True), primary_key=True)
    unit_type_name = Column(String(128))