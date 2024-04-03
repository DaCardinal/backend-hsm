from sqlalchemy import Numeric, create_engine, Column, ForeignKey, Boolean, DateTime, Enum, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from app.models.model_base import BaseModel as Base
import enum

class Message(Base):
    __tablename__ = 'message'
    message_id = Column(UUID(as_uuid=True), primary_key=True)
    subject = Column(String(128))
    sender_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'))
    message_body = Column(Text)
    date_created = Column(DateTime)
    parent_message_id = Column(UUID(as_uuid=True), ForeignKey('message.message_id'))
    is_draft = Column(Boolean, default=True)
    is_notification = Column(Boolean, default=False)
    is_reminder = Column(Boolean)
    next_remind_date = Column(DateTime)
    reminder_frequency_id = Column(UUID(as_uuid=True), ForeignKey('reminder_frequency.id'))
