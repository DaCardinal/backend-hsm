from sqlalchemy import Numeric, create_engine, Column, ForeignKey, Boolean, DateTime, Enum, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from app.models.model_base import BaseModel as Base
import enum

class PaymentStatusEnum(enum.Enum):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"

class Invoice(Base):
    __tablename__ = 'invoice'
    invoice_number = Column(String(128), primary_key=True, unique=True)
    issued_by = Column(String)
    issued_to = Column(String)
    invoice_details = Column(Text)
    invoice_amount = Column(Numeric(10, 2))
    invoice_item = Column(String(128))  # [property, property_unit, maintenance, service, fee]
    date_created = Column(DateTime)
    billing_date = Column(DateTime)
    date_paid = Column(DateTime)
    status = Column(Enum(PaymentStatusEnum))
    transaction_id = Column(UUID(as_uuid=True), ForeignKey('transaction.transaction_id'))

    contracts = relationship('Contract', secondary='contract_invoice', back_populates='invoices')
    transaction = relationship('Transaction', back_populates='invoice_number')