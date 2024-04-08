from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.models.model_base import BaseModel as Base

class ContractDocuments(Base):
    __tablename__ = 'contract_documents'
    id = Column(UUID(as_uuid=True), primary_key=True)
    contract_id = Column(UUID(as_uuid=True), ForeignKey('contract.contract_id'))
    document_number = Column(UUID(as_uuid=True), ForeignKey('documents.document_number'))