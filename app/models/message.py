import uuid
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, ForeignKey, Boolean, DateTime, String, Text, func, UUID

from app.models.model_base import BaseModel as Base

class Message(Base):
    __tablename__ = 'message'

    message_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subject = Column(String(128))
    sender_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'))
    message_body = Column(Text)
    parent_message_id = Column(UUID(as_uuid=True), ForeignKey('message.message_id'), nullable=True)
    thread_id = Column(UUID(as_uuid=True), ForeignKey('message.message_id'), nullable=True)
    is_draft = Column(Boolean, default=False, nullable=True)
    is_notification = Column(Boolean, default=False, nullable=True)
    is_reminder = Column(Boolean, default=False, nullable=True)
    is_scheduled = Column(Boolean, default=False, nullable=True)
    is_read = Column(Boolean, default=False, nullable=True)
    date_created = Column(DateTime(timezone=True), default=func.now())
    scheduled_date = Column(DateTime(timezone=True), default=func.now())
    next_remind_date = Column(DateTime(timezone=True), nullable=True)

    # TODO: Add to next update on message model
    reminder_frequency_id = Column(UUID(as_uuid=True), ForeignKey('reminder_frequency.id'))
    reminder_frequency = relationship('ReminderFrequency', back_populates='messages')

    sender = relationship('User', back_populates='sent_messages', lazy='selectin')
    
    recipients = relationship('MessageRecipient', back_populates='message', lazy='selectin')

    replies = relationship('Message',
                           backref=backref('parent_message', remote_side=[message_id]),
                           foreign_keys=[parent_message_id],
                           cascade='all, delete-orphan')
    
    thread = relationship('Message', remote_side=[message_id],
                          backref=backref('thread_messages', foreign_keys=[thread_id]),
                          foreign_keys=[thread_id])