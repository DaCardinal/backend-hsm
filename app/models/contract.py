import uuid
import enum
import datetime
from sqlalchemy.orm import relationship, column_property
from sqlalchemy import (
    Numeric,
    String,
    event,
    Column,
    ForeignKey,
    DateTime,
    Enum,
    Integer,
    Text,
    UUID,
    select,
)

from app.models.model_base import BaseModel as Base
from app.models.contract_type import ContractType
from app.models.payment_type import PaymentTypes


class ContractStatusEnum(enum.Enum):
    active = "active"
    inactive = "inactive"
    expired = "expired"
    pending = "pending"
    terminated = "terminated"


class Contract(Base):
    __tablename__ = "contract"

    contract_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4,
    )
    contract_number = Column(String(128), unique=True, nullable=False)
    contract_type_id = Column(
        UUID(as_uuid=True), ForeignKey("contract_type.contract_type_id")
    )
    payment_type_id = Column(
        UUID(as_uuid=True), ForeignKey("payment_types.payment_type_id")
    )  # [one_time, monthly, quarterly, semi_annual, annual]
    contract_status = Column(Enum(ContractStatusEnum))
    contract_details = Column(Text)
    num_invoices = Column(Integer, default=0)
    payment_amount = Column(Numeric(10, 2))
    fee_percentage = Column(Numeric(5, 2))
    fee_amount = Column(Numeric(10, 2))
    date_signed = Column(DateTime(timezone=True))
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))

    # generate dynamic column property
    contract_type_value = column_property(
        select(ContractType.contract_type_name)
        .where(ContractType.contract_type_id == contract_type_id)
        .correlate_except(ContractType)
        .scalar_subquery()
    )

    payment_type_value = column_property(
        select(PaymentTypes.payment_type_name)
        .where(PaymentTypes.payment_type_id == payment_type_id)
        .correlate_except(PaymentTypes)
        .scalar_subquery()
    )

    contract_documents = relationship(
        "Documents", secondary="contract_documents", back_populates="contract"
    )
    invoices = relationship(
        "Invoice", secondary="contract_invoice", back_populates="contracts"
    )
    # under_contract = relationship(
    #     "UnderContract", back_populates="contract", lazy="selectin"
    # )
    under_contract = relationship(
        "UnderContract",
        back_populates="contract",
        lazy="selectin",
        foreign_keys='UnderContract.contract_id',
        cascade="all, delete-orphan",
        viewonly=True
    )

    properties = relationship(
        "PropertyUnitAssoc",
        secondary="under_contract",
        primaryjoin="Contract.contract_id == UnderContract.contract_id",
        secondaryjoin="UnderContract.property_unit_assoc_id == PropertyUnitAssoc.property_unit_assoc_id",
        foreign_keys="[Contract.contract_id, PropertyUnitAssoc.property_unit_assoc_id]",
        lazy="selectin",
    )

    # relationship to utilities
    utilities = relationship(
        "EntityBillable",
        primaryjoin="and_(EntityBillable.entity_assoc_id==Contract.contract_id, EntityBillable.entity_type=='Contract', EntityBillable.billable_type=='Utilities')",
        foreign_keys="[EntityBillable.entity_assoc_id]",
        overlaps="entity_billable,utilities",
        lazy="selectin",
        viewonly=True,
    )

    contract_type = relationship(
        "ContractType", back_populates="contracts", lazy="selectin"
    )
    payment_type = relationship(
        "PaymentTypes", back_populates="contracts", lazy="selectin"
    )

    def to_dict(self, exclude=[]):
        if exclude is None:
            exclude = set()
        data = {}
        self.contract_type_value

        for key in self.__dict__.keys():
            if not key.startswith("_") and key not in exclude:
                value = getattr(self, key)
                if key == "contract_type_id":
                    data["contract_type_value"] = self.contract_type_value
                    continue
                if key == "payment_type_id":
                    data["payment_type_value"] = self.payment_type_value
                    continue
                if isinstance(value, UUID):
                    value = str(value)
                data[key] = value

        return data


@event.listens_for(Contract, "before_insert")
def receive_before_insert(mapper, connection, target):
    if not target.contract_number:
        current_time_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        target.contract_number = f"CTR{current_time_str}"


@event.listens_for(Contract, "after_insert")
def receive_after_insert(mapper, connection, target):
    if not target.contract_number:
        current_time_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        target.contract_number = f"CTR{current_time_str}"
        connection.execute(
            target.__table__.update()
            .where(target.__table__.c.contract_id == target.contract_id)
            .values(contract_number=target.contract_number)
        )
