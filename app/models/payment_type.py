from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.model_base import BaseModel as Base

class PaymentTypes(Base):
    __tablename__ = 'payment_types'
    payment_type_id = Column(UUID(as_uuid=True), primary_key=True)
    payment_type_name = Column(String(80))
    payment_type_description = Column(Text)

    unit_utilities = relationship('UnitUtilities', back_populates='payment_type')
    contracts = relationship('Contract', back_populates='payment_type')