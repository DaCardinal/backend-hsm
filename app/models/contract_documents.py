from sqlalchemy import Numeric, create_engine, Column, ForeignKey, Boolean, DateTime, Enum, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from app.models.model_base import BaseModel as Base
import enum


class ContractDocuments(Base):
    __tablename__ = 'contract_documents'
    id = Column(UUID(as_uuid=True), primary_key=True)
    contract_id = Column(UUID(as_uuid=True), ForeignKey('contract.contract_id'))
    document_number = Column(UUID(as_uuid=True))