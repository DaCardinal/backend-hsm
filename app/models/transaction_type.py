import uuid
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, UUID

from app.models.model_base import BaseModel as Base

class TransactionType(Base):
    __tablename__ = 'transaction_type'
    
    transaction_type_id = Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True, default=uuid.uuid4)
    transaction_type_name = Column(String(128), unique=True, index=True)
    transaction_type_description = Column(String(128))

    transactions = relationship('Transaction', back_populates='transaction_type')