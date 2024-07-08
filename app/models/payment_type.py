import uuid
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Numeric, String, Text, UUID

from app.models.model_base import BaseModel as Base

class PaymentTypes(Base):
    __tablename__ = 'payment_types'
    
    payment_type_id = Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True, default=uuid.uuid4)
    payment_type_name = Column(String(80))
    payment_type_description = Column(Text)
    num_of_invoices = Column(Numeric(10, 2))

    entity_billable = relationship('EntityBillable', back_populates='payment_type')
    contracts = relationship('Contract', back_populates='payment_type')