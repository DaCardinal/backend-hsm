from sqlalchemy import Column, ForeignKey, Boolean, DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref
from app.models.model_base import BaseModel as Base

class Message(Base):
    __tablename__ = 'message'
    message_id = Column(UUID(as_uuid=True), primary_key=True)
    subject = Column(String(128))
    sender_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'))
    message_body = Column(Text)
    parent_message_id = Column(UUID(as_uuid=True), ForeignKey('message.message_id'))
    is_draft = Column(Boolean, default=True)
    is_notification = Column(Boolean, default=False)
    is_reminder = Column(Boolean, default=False)
    date_created = Column(DateTime(timezone=True), default=func.now())
    next_remind_date = Column(DateTime(timezone=True), default=func.now())
    reminder_frequency_id = Column(UUID(as_uuid=True), ForeignKey('reminder_frequency.id'))

    sender = relationship('User', back_populates='sent_messages')
    recipients = relationship('MessageRecipient', back_populates='message')
    replies = relationship('Message',
                           backref=backref('parent_message', remote_side=[message_id]),
                           cascade='all, delete-orphan')
    reminder_frequency = relationship('ReminderFrequency', back_populates='messages')