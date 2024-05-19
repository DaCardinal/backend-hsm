import uuid
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Numeric, Column, ForeignKey, String, UUID

from app.models.model_base import BaseModel as Base


class InvoiceItem(Base):
    __tablename__ = 'invoice_items'

    invoice_item_id = Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True, default=uuid.uuid4)
    invoice_number = Column(String(128), ForeignKey('invoice.invoice_number'), nullable=False)
    description = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)

    invoice = relationship("Invoice", back_populates="invoice_items", lazy='selectin')