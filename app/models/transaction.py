from sqlalchemy import Column, ForeignKey, DateTime, Enum, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.models.model_base import BaseModel as Base

class PaymentStatusEnum(enum.Enum):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"

class Transaction(Base):
    __tablename__ = 'transaction'
    transaction_id = Column(UUID(as_uuid=True), primary_key=True)
    transaction_type_id = Column(UUID(as_uuid=True), ForeignKey('transaction_type.transaction_type_id'))
    client_offered = Column(UUID(as_uuid=True), ForeignKey('users.user_id'))
    client_requested = Column(UUID(as_uuid=True), ForeignKey('users.user_id'))
    transaction_date = Column(DateTime)
    transaction_details = Column(Text)
    payment_method = Column(String)
    transaction_status = Column(Enum(PaymentStatusEnum))
    invoice_number = Column(UUID(as_uuid=True), ForeignKey('invoice.invoice_number'))

    transaction_type = relationship('TransactionType', back_populates='transactions')

    client_offered_transaction = relationship('User', foreign_keys=[client_offered], back_populates='transaction_as_client_offered')
    client_requested_transaction = relationship('User', foreign_keys=[client_requested], back_populates='transaction_as_client_requested')

    invoice_number = relationship('Invoice', back_populates='transaction')