from sqlalchemy import Numeric, create_engine, Column, ForeignKey, Boolean, DateTime, Enum, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from app.models.model_base import BaseModel as Base
import enum

class Utilities(Base):
    __tablename__ = 'utilities'
    utility_id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(128))
    description = Column(String(50))