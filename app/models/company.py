from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, UUID

from app.models.model_base import BaseModel as Base

class Company(Base):
    __tablename__ = 'company'
    
    company_id = Column(UUID(as_uuid=True), primary_key=True)
    company_name = Column(String(80))
    company_website = Column(String(80))

    users = relationship('User', secondary='users_company', back_populates="company")