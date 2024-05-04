import uuid
from sqlalchemy import Column, ForeignKey, String, UUID
from sqlalchemy.orm import relationship

from app.models.model_base import BaseModel as Base

class EntityMedia(Base):
    __tablename__ = 'entity_media'
    entity_assoc_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_type = Column(String(80))
    entity_id = Column(UUID(as_uuid=True), primary_key=True)
    media_id = Column(UUID(as_uuid=True), ForeignKey('media.media_id'), primary_key=True)

    media = relationship('Media', back_populates='entity_media', overlaps="units_amenities,property_unit_assoc")