from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.model_base import BaseModel as Base

class Amenities(Base):
    __tablename__ = 'amenities'
    amenity_id = Column(UUID(as_uuid=True), primary_key=True)
    amenity_name = Column(String(128))
    amenity_short_name = Column(String(80))
    amenity_value_type = Column(String(50))  # enum? boolean, integer
    description = Column(Text)
    deleted_at = Column(DateTime(timezone=True))

    units = relationship("PropertyUnitAssoc", secondary="units_amenities", back_populates="amenities")