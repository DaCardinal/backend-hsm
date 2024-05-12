from sqlalchemy import Column, ForeignKey, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.model_base import BaseModel as Base
import enum

class ContractStatusEnum(enum.Enum):
    active = "active"
    expired = "expired"
    terminated = "terminated"

class UnderContract(Base):
    __tablename__ = 'under_contract'
    id = Column(UUID(as_uuid=True), primary_key=True)
    property_unit_assoc_id = Column(UUID(as_uuid=True), ForeignKey('property_unit_assoc.property_unit_assoc_id'))
    contract_id = Column(UUID(as_uuid=True), ForeignKey('contract.contract_id'))
    contract_status = Column(Enum(ContractStatusEnum))
    client_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'))
    employee_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'))
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))

    properties  = relationship('PropertyUnitAssoc', back_populates='under_contract')
    contract  = relationship('Contract', back_populates='under_contract')

    client_representative = relationship('User', foreign_keys=[client_id], back_populates='client_under_contract')
    employee_representative = relationship('User', foreign_keys=[employee_id], back_populates='employee_under_contract')