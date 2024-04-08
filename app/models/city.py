from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.model_base import BaseModel as Base


class City(Base):
    __tablename__ = 'city'
    city_id = Column(UUID(as_uuid=True), primary_key=True)
    city_name = Column(String(128))

    addresses = relationship('Addresses', back_populates='city')