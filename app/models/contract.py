from sqlalchemy import Numeric, create_engine, Column, ForeignKey, Boolean, DateTime, Enum, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from app.models.model_base import BaseModel as Base
import enum

class ContractStatusEnum(enum.Enum):
    active = "active"
    expired = "expired"
    terminated = "terminated"

class Contract(Base):
    __tablename__ = 'contract'
    contract_id = Column(UUID(as_uuid=True), primary_key=True)
    contract_type_id = Column(UUID(as_uuid=True), ForeignKey('contract_type.contract_type_id'))
    contract_details = Column(UUID(as_uuid=True))
    payment_type_id = Column(UUID(as_uuid=True), ForeignKey('payment_types.payment_type_id'))
    num_invoices = Column(Integer)
    payment_amount = Column(Numeric(10, 2))
    fee_percentage = Column(Numeric(5, 2))
    fee_amount = Column(Numeric(10, 2))
    date_signed = Column(DateTime)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    contract_status = Column(Enum(ContractStatusEnum))
    transaction_id = Column(UUID(as_uuid=True))