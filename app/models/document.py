from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, String, UUID

from app.models.model_base import BaseModel as Base

class Documents(Base):
    __tablename__ = 'documents'

    document_number = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(128))
    content_url = Column(String(128))
    content_type = Column(String(128))
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey('users.user_id'))

    users = relationship('User', back_populates="documents")
    contract = relationship('Contract', secondary='contract_documents', back_populates='contract_documents')