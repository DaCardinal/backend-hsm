from sqlalchemy import create_engine, Column, ForeignKey, Boolean, DateTime, Enum, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from app.models.model_base import BaseModel as Base

class Company(Base):
    __tablename__ = 'company'
    company_id = Column(UUID(as_uuid=True), primary_key=True)
    company_name = Column(String(80))
    company_website = Column(String(80))

    users = relationship("UsersCompany", back_populates="company")