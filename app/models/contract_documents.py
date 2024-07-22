import uuid
from sqlalchemy import Column, ForeignKey, UUID

from app.models.model_base import BaseModel as Base


class ContractDocuments(Base):
    __tablename__ = "contract_documents"

    contract_document_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4,
    )
    contract_id = Column(UUID(as_uuid=True), ForeignKey("contract.contract_id"))
    document_number = Column(
        UUID(as_uuid=True), ForeignKey("documents.document_number")
    )
