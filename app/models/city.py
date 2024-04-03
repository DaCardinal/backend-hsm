from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from app.models.model_base import BaseModel as Base


class City(Base):
    __tablename__ = 'city'
    city_id = Column(UUID(as_uuid=True), primary_key=True)
    city_name = Column(String(128))
    country_id = Column(UUID(as_uuid=True), ForeignKey('country.country_id'))