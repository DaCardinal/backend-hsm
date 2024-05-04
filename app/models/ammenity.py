import uuid
from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.model_base import BaseModel as Base

class Amenities(Base):
    __tablename__ = 'amenities'
    amenity_id = Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True, default=uuid.uuid4)
    amenity_name = Column(String(128))
    amenity_short_name = Column(String(80))
    amenity_value_type = Column(String(50))  # enum? boolean, integer
    description = Column(Text)

    units = relationship("PropertyUnitAssoc", secondary="units_amenities", back_populates="amenities", overlaps="ammenities")
    media = relationship("Media",
                         secondary="entity_media",
                         primaryjoin="and_(EntityMedia.entity_id==Amenities.amenity_id, EntityMedia.entity_type=='Amenities')",
                         overlaps="entity_media,media",
                         lazy="selectin")