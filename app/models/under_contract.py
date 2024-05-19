import uuid
import enum
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Enum, UUID

from app.models.model_base import BaseModel as Base

class ContractStatusEnum(enum.Enum):
    active = "active"
    expired = "expired"
    terminated = "terminated"
    pending = "pending"

class UnderContract(Base):
    __tablename__ = 'under_contract'

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True, default=uuid.uuid4)
    property_unit_assoc_id = Column(UUID(as_uuid=True), ForeignKey('property_unit_assoc.property_unit_assoc_id'))
    contract_id = Column(UUID(as_uuid=True), ForeignKey('contract.contract_id'))
    contract_status = Column(Enum(ContractStatusEnum))
    client_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'), nullable=True)
    employee_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'), nullable=True)

    properties  = relationship('PropertyUnitAssoc', back_populates='under_contract', lazy='selectin')
    contract  = relationship('Contract', back_populates='under_contract', lazy='selectin')

    client_representative = relationship('User', foreign_keys=[client_id], back_populates='client_under_contract', lazy='selectin')
    employee_representative = relationship('User', foreign_keys=[employee_id], back_populates='employee_under_contract', lazy='selectin')