from sqlalchemy import create_engine, Column, ForeignKey, Boolean, DateTime, Enum, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from app.models.model_base import BaseModel as Base


class ReminderFrequency(Base):
    __tablename__ = 'reminder_frequency'
    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(String(50))
    frequency = Column(Integer)
    is_active = Column(Boolean, default=False)