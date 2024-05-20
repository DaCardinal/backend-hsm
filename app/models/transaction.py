import uuid
import enum
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, DateTime, Enum, String, Text, UUID

from app.models.model_base import BaseModel as Base

class PaymentStatusEnum(enum.Enum):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"

class Transaction(Base):
    __tablename__ = 'transaction'
    
    transaction_id = Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True, default=uuid.uuid4)
    transaction_type_id = Column(String, ForeignKey('transaction_type.transaction_type_name'))
    client_offered = Column(UUID(as_uuid=True), ForeignKey('users.user_id')) # payer_id
    client_requested = Column(UUID(as_uuid=True), ForeignKey('users.user_id')) # payee_id
    transaction_date = Column(DateTime)
    transaction_details = Column(Text)
    payment_method = Column(String)
    transaction_status = Column(Enum(PaymentStatusEnum))
    invoice_number = Column(String(128), ForeignKey('invoice.invoice_number'))

    transaction_type = relationship('TransactionType', back_populates='transactions')

    client_offered_transaction = relationship('User', foreign_keys=[client_offered], back_populates='transaction_as_client_offered')
    client_requested_transaction = relationship('User', foreign_keys=[client_requested], back_populates='transaction_as_client_requested')

    # invoice_number = relationship('Invoice', back_populates='transaction', lazy="selectin")
    transaction_invoice = relationship('Invoice', primaryjoin="and_(Invoice.invoice_number==Transaction.invoice_number)", back_populates='transaction')