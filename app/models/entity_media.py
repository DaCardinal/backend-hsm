import uuid
from sqlalchemy import Column, ForeignKey, String, UUID

from app.models.model_base import BaseModel as Base

class EntityMedia(Base):
    __tablename__ = 'entity_media'
    
    entity_assoc_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_type = Column(String(80)) # TODO [Types: units, property, amenities, documents]
    media_assoc_id = Column(UUID(as_uuid=True)) # [property_unit_assoc_id | entity_ammenity_id | document_id ]
    media_id = Column(UUID(as_uuid=True), ForeignKey('media.media_id'), primary_key=True)