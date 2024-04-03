from sqlalchemy import Numeric, create_engine, Column, ForeignKey, Boolean, DateTime, Enum, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from app.models.model_base import BaseModel as Base
import enum

class ContractInvoice(Base):
    __tablename__ = 'contract_invoice'
    contract_id = Column(UUID(as_uuid=True), ForeignKey('contract.contract_id'))
    invoice_number = Column(String(128), ForeignKey('invoice.invoice_number'), primary_key=True)