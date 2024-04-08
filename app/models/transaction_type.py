from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.model_base import BaseModel as Base

class TransactionType(Base):
    __tablename__ = 'transaction_type'
    transaction_type_id = Column(UUID(as_uuid=True), primary_key=True)
    transaction_type_name = Column(String(128))

    transactions = relationship('Transaction', back_populates='transaction_type')