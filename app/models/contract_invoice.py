import uuid
from sqlalchemy import Column, ForeignKey, String, UUID

from app.models.model_base import BaseModel as Base

class ContractInvoice(Base):
    __tablename__ = 'contract_invoice'

    contract_invoice_id = Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True, default=uuid.uuid4)
    contract_id = Column(UUID(as_uuid=True), ForeignKey('contract.contract_id'))
    invoice_number = Column(String(128), ForeignKey('invoice.invoice_number'), primary_key=True)