from sqlalchemy import Numeric, create_engine, Column, ForeignKey, Boolean, DateTime, Enum, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from app.models.model_base import BaseModel as Base
import enum


class MessageRecipient(Base):
    __tablename__ = 'message_recipient'
    id = Column(UUID(as_uuid=True), primary_key=True)
    recipient_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'))
    recipient_group_id = Column(UUID(as_uuid=True), ForeignKey('property_unit_assoc.property_unit_assoc'))
    message_id = Column(UUID(as_uuid=True), ForeignKey('message.message_id'))
    is_read = Column(Boolean)