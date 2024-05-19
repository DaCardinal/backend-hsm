import uuid
import enum
from sqlalchemy.orm import relationship, column_property
from sqlalchemy import Numeric, Column, ForeignKey, DateTime, Enum, Integer, Text, UUID, select

from app.models.model_base import BaseModel as Base
from app.models import ContractType, PaymentTypes

class ContractStatusEnum(enum.Enum):
    active = "active"
    expired = "expired"
    terminated = "terminated"
    pending = "pending"

class Contract(Base):
    __tablename__ = 'contract'

    contract_id = Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True, default=uuid.uuid4)
    contract_type_id = Column(UUID(as_uuid=True), ForeignKey('contract_type.contract_type_id'))
    payment_type_id = Column(UUID(as_uuid=True), ForeignKey('payment_types.payment_type_id'))
    contract_status = Column(Enum(ContractStatusEnum))
    contract_details = Column(Text)
    num_invoices = Column(Integer)
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

    contract_documents = relationship('Documents', secondary='contract_documents', back_populates='contract')
    invoices = relationship('Invoice', secondary='contract_invoice', back_populates='contracts')
    under_contract = relationship('UnderContract', back_populates='contract', lazy='selectin')

    contract_type = relationship('ContractType', back_populates='contracts', lazy='selectin')
    payment_type = relationship('PaymentTypes', back_populates='contracts', lazy='selectin')

    def to_dict(self, exclude=[]):
        if exclude is None:
            exclude = set()
        data = {}
        self.contract_type_value

        for key in self.__dict__.keys():
            if not key.startswith("_") and key not in exclude:
                value = getattr(self, key)
                if key == 'contract_type_id':
                    data['contract_type_value'] = self.contract_type_value
                    continue
                if key == 'payment_type_id':
                    data['payment_type_value'] = self.payment_type_value
                    continue
                if isinstance(value, UUID):
                    value = str(value)
                data[key] = value

        return data