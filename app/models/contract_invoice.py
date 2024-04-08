from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from app.models.model_base import BaseModel as Base

class ContractInvoice(Base):
    __tablename__ = 'contract_invoice'
    contract_id = Column(UUID(as_uuid=True), ForeignKey('contract.contract_id'))
    invoice_number = Column(String(128), ForeignKey('invoice.invoice_number'), primary_key=True)