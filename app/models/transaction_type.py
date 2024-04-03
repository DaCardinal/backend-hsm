from sqlalchemy import Numeric, create_engine, Column, ForeignKey, Boolean, DateTime, Enum, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from app.models.model_base import BaseModel as Base
import enum

class TransactionType(Base):
    __tablename__ = 'transaction_type'
    transaction_type_id = Column(UUID(as_uuid=True), primary_key=True)
    transaction_type_name = Column(String(128))