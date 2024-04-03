from sqlalchemy import Numeric, create_engine, Column, ForeignKey, Boolean, DateTime, Enum, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from app.models.model_base import BaseModel as Base
import enum

class Amenities(Base):
    __tablename__ = 'amenities'
    amenity_id = Column(UUID(as_uuid=True), primary_key=True)
    amenity_name = Column(String(128))
    amenity_short_name = Column(String(80))
    amenity_value_type = Column(String(50))  # enum? boolean, integer
    description = Column(Text)
    date_created = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)