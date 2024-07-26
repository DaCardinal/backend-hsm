import enum
import uuid
import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, DateTime, Enum, String, Text, UUID, event

from app.models.model_base import BaseModel as Base


class PaymentStatusEnum(enum.Enum):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"
    reversal = "reversal"


class Transaction(Base):
    __tablename__ = "transaction"

    transaction_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4,
    )
    transaction_number = Column(String(128), unique=True, nullable=False)
    payment_method = Column(String, ForeignKey("payment_types.payment_type_name"))
    client_offered = Column(
        UUID(as_uuid=True), ForeignKey("users.user_id")
    )  # payer_name
    client_requested = Column(
        UUID(as_uuid=True), ForeignKey("users.user_id")
    )  # payee_name
    transaction_date = Column(DateTime)
    transaction_details = Column(Text)
    transaction_type = Column(
        String(128), ForeignKey("transaction_type.transaction_type_name")
    )
    transaction_status = Column(Enum(PaymentStatusEnum))
    invoice_number = Column(
        String(128),
        ForeignKey(
            "invoice.invoice_number",
            use_alter=True,
            name="fk_transaction_invoice_number",
        ),
    )

    transaction_types = relationship("TransactionType", back_populates="transactions")

    client_offered_transaction = relationship(
        "User",
        foreign_keys=[client_offered],
        back_populates="transaction_as_client_offered",
        lazy="selectin",
    )
    client_requested_transaction = relationship(
        "User",
        foreign_keys=[client_requested],
        back_populates="transaction_as_client_requested",
        lazy="selectin",
    )

    transaction_invoice = relationship(
        "Invoice",
        primaryjoin="Invoice.invoice_number==Transaction.invoice_number",
        back_populates="transaction",
        lazy="selectin",
    )


@event.listens_for(Transaction, "before_insert")
def receive_before_insert(mapper, connection, target):
    if not target.transaction_number:
        current_time_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        target.transaction_number = f"TRANS{current_time_str}"


@event.listens_for(Transaction, "after_insert")
def receive_after_insert(mapper, connection, target):
    if not target.transaction_number:
        current_time_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        target.transaction_number = f"TRANS{current_time_str}"
        connection.execute(
            target.__table__.update()
            .where(target.__table__.c.id == target.id)
            .values(transaction_number=target.transaction_number)
        )
