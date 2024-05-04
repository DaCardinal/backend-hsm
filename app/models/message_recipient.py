from sqlalchemy import Column, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.model_base import BaseModel as Base

class MessageRecipient(Base):
    __tablename__ = 'message_recipient'
    id = Column(UUID(as_uuid=True), primary_key=True)
    recipient_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'))
    recipient_group_id = Column(UUID(as_uuid=True), ForeignKey('property_unit_assoc.property_unit_assoc_id'))
    message_id = Column(UUID(as_uuid=True), ForeignKey('message.message_id'))
    is_read = Column(Boolean)

    receipient = relationship('User', back_populates='received_messages')
    message = relationship('Message', back_populates='recipients')
    message_group = relationship('PropertyUnitAssoc', back_populates="messages_recipients")