from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID

from app.models.model_base import BaseModel as Base

class Country(Base):
    __tablename__ = 'country'
    country_id = Column(UUID(as_uuid=True), primary_key=True)
    country_name = Column(String(128))
    description = Column(Text)
