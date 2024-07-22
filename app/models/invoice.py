import enum
import uuid
import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    String,
    event,
    Numeric,
    ForeignKey,
    DateTime,
    Enum,
    Text,
    UUID,
)

from app.models.model_base import BaseModel as Base


class PaymentStatusEnum(enum.Enum):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"


class Invoice(Base):
    __tablename__ = "invoice"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4,
    )
    invoice_number = Column(String(128), unique=True, nullable=False)
    issued_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id", use_alter=True, name="fk_invoice_issued_by"),
    )
    issued_to = Column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id", use_alter=True, name="fk_invoice_issued_to"),
    )
    invoice_details = Column(Text)
    invoice_amount = Column(Numeric(10, 2))
    due_date = Column(DateTime)
    date_paid = Column(DateTime)
    status = Column(Enum(PaymentStatusEnum), default=PaymentStatusEnum.pending)
    transaction_id = Column(
        UUID(as_uuid=True),
        ForeignKey("transaction.transaction_id", ondelete="CASCADE"),
        nullable=True,
    )

    contracts = relationship(
        "Contract", secondary="contract_invoice", back_populates="invoices"
    )
    transaction = relationship(
        "Transaction",
        primaryjoin="Invoice.invoice_number==Transaction.invoice_number",
        back_populates="transaction_invoice",
        lazy="selectin",
    )
    invoice_items = relationship(
        "InvoiceItem", back_populates="invoice", lazy="selectin"
    )  # [property, property_unit, maintenance, service, fee]

    issued_by_user = relationship(
        "User",
        foreign_keys=[issued_by],
        backref="invoice_as_issued_by_user",
        lazy="selectin",
    )
    issued_to_user = relationship(
        "User",
        foreign_keys=[issued_to],
        backref="invoice_as_issued_to_user",
        lazy="selectin",
    )


@event.listens_for(Invoice, "before_insert")
def receive_before_insert(mapper, connection, target):
    if not target.invoice_number:
        current_time_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        target.invoice_number = f"INV{current_time_str}"


@event.listens_for(Invoice, "after_insert")
def receive_after_insert(mapper, connection, target):
    if not target.invoice_number:
        current_time_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        target.invoice_number = f"INV{current_time_str}"
        connection.execute(
            target.__table__.update()
            .where(target.__table__.c.id == target.id)
            .values(invoice_number=target.invoice_number)
        )


@event.listens_for(Invoice, "after_insert")
@event.listens_for(Invoice, "after_update")
def update_invoice_amount(mapper, connection, target):
    total_amount = sum(item.total_price for item in target.invoice_items)
    connection.execute(
        target.__table__.update()
        .where(target.__table__.c.id == target.id)
        .values(invoice_amount=total_amount)
    )
