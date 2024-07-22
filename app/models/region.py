import uuid
from sqlalchemy.orm import relationship
from sqlalchemy import UUID, Column, ForeignKey, String

from app.models.model_base import BaseModel as Base


class Region(Base):
    __tablename__ = "region"

    region_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    country_id = Column(UUID(as_uuid=True), ForeignKey("country.country_id"))
    region_name = Column(String(128))

    addresses = relationship("Addresses", back_populates="region")
    country = relationship("Country", back_populates="region")
    city = relationship("City", back_populates="region")
