import uuid
from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, ForeignKey, Boolean, UUID

from app.models.model_base import BaseModel as Base

class MessageRecipient(Base):
    __tablename__ = 'message_recipient'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recipient_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'))
    recipient_group_id = Column(UUID(as_uuid=True), ForeignKey('property_unit_assoc.property_unit_assoc_id'), nullable=True)
    message_id = Column(UUID(as_uuid=True), ForeignKey('message.message_id'))
    is_read = Column(Boolean)
    msg_send_date = Column(DateTime(timezone=True))

    recipient = relationship('User', back_populates='received_messages', lazy='selectin')
    message = relationship('Message', back_populates='recipients', lazy='selectin')
    message_group = relationship('PropertyUnitAssoc', back_populates="messages_recipients", lazy='selectin')