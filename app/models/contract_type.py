from sqlalchemy import Numeric, Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.model_base import BaseModel as Base

class ContractType(Base):
    __tablename__ = 'contract_type'
    contract_type_id = Column(UUID(as_uuid=True), primary_key=True)
    contract_type_name = Column(String(128))
    fee_percentage = Column(Numeric(5, 2))

    contracts = relationship('Contract', back_populates='contract_type')