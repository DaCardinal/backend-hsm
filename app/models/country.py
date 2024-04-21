import uuid
from sqlalchemy import Column, String, Text, UUID
from sqlalchemy.orm import relationship

from app.models.model_base import BaseModel as Base

class Country(Base):
    __tablename__ = 'country'
    country_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    country_name = Column(String(128), unique=True)

    addresses = relationship('Addresses', back_populates='country')
    region = relationship('Region', back_populates='country')