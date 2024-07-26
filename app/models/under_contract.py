import uuid
import enum
from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, ForeignKey, Enum, UUID, String

from app.models.model_base import BaseModel as Base


class ContractStatusEnum(enum.Enum):
    active = "active"
    inactive = "inactive"
    expired = "expired"
    terminated = "terminated"
    pending = "pending"


class UnderContract(Base):
    __tablename__ = "under_contract"

    under_contract_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4,
    )
    property_unit_assoc_id = Column(
        UUID(as_uuid=True), ForeignKey("property_unit_assoc.property_unit_assoc_id")
    )
    contract_status = Column(Enum(ContractStatusEnum))
    contract_id = Column(
        String(80), ForeignKey("contract.contract_number", ondelete="CASCADE")
    )
    client_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=True)
    employee_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=True)
    start_date = Column(
        DateTime(timezone=True)
    )  # TODO: Value determined by contract start date
    end_date = Column(
        DateTime(timezone=True)
    )  # TODO: Value determined by contract end date
    next_payment_due = Column(
        DateTime(timezone=True)
    )  # TODO: Value determined by system

    properties = relationship(
        "PropertyUnitAssoc", back_populates="under_contract", lazy="selectin"
    )
    contract = relationship(
        "Contract",
        back_populates="under_contract",
        lazy="selectin",
        foreign_keys=[contract_id],
        viewonly=True,
    )

    client_representative = relationship(
        "User",
        foreign_keys=[client_id],
        back_populates="client_under_contract",
        lazy="selectin",
    )
    employee_representative = relationship(
        "User",
        foreign_keys=[employee_id],
        back_populates="employee_under_contract",
        lazy="selectin",
    )
