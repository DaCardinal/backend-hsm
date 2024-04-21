import uuid
from sqlalchemy import Column, ForeignKey, String, UUID
from sqlalchemy.orm import relationship

from app.models.model_base import BaseModel as Base


class City(Base):
    __tablename__ = 'city'
    city_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    region_id = Column(UUID(as_uuid=True), ForeignKey('region.region_id'))
    city_name = Column(String(128))

    addresses = relationship('Addresses', back_populates='city')
    region = relationship('Region', back_populates='city')