from sqlalchemy import create_engine, Column, ForeignKey, Boolean, DateTime, Enum, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from app.models.model_base import BaseModel as Base

class EntityAddress(Base):
    __tablename__ = 'entity_address'
    entity_assoc_id = Column(UUID(as_uuid=True), primary_key=True)
    entity_type = Column(String(80))
    entity_id = Column(UUID(as_uuid=True))
    address_id = Column(UUID(as_uuid=True), ForeignKey('addresses.address_id'))
    emergency_address = Column(Boolean, default=False)
    emergency_address_hash = Column(UUID(as_uuid=True), default="")