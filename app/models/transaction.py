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
