from sqlalchemy import Numeric, create_engine, Column, ForeignKey, Boolean, DateTime, Enum, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
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
    property_unit_assoc = Column(UUID(as_uuid=True), ForeignKey('property_unit_assoc.property_unit_assoc'))
    contract_id = Column(UUID(as_uuid=True), ForeignKey('contract.contract_id'))
    contract_status = Column(Enum(ContractStatusEnum))
    client_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'))
    employee_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'))