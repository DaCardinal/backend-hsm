import uuid
from importlib import import_module
from sqlalchemy.orm import relationship, Session
from sqlalchemy import Column, String, event, Integer, Numeric, Column, ForeignKey, String, UUID

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


@event.listens_for(InvoiceItem, 'before_insert')
@event.listens_for(InvoiceItem, 'before_update')
def calculate_total_price(mapper, connection, target: InvoiceItem):
    # Calculate the total price as unit_price * quantity
    target.total_price = target.unit_price * target.quantity

@event.listens_for(InvoiceItem, 'after_insert')
@event.listens_for(InvoiceItem, 'after_update')
@event.listens_for(InvoiceItem, 'after_delete')
def update_invoice_after_item_change(mapper, connection, target: InvoiceItem):
    # Update the invoice amount when an invoice item is added, updated, or deleted
    models_module = import_module("app.models")
    invoice_model = getattr(models_module, "Invoice")
    
    session = Session(connection)
    invoice = session.query(invoice_model).filter_by(invoice_number=target.invoice_number).first()

    if invoice:
        total_amount = sum(item.total_price for item in invoice.invoice_items)
        connection.execute(
            invoice.__table__.update()
            .where(invoice.__table__.c.invoice_number == invoice.invoice_number)
            .values(invoice_amount=total_amount)
        )
    session.close()