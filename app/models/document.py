from sqlalchemy import Numeric, create_engine, Column, ForeignKey, Boolean, DateTime, Enum, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from app.models.model_base import BaseModel as Base
import enum

class Documents(Base):
    __tablename__ = 'documents'
    document_number = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(128))
    content_url = Column(String(128))
    content_type = Column(String(128))
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey('users.user_id'))