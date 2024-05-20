import uuid
from sqlalchemy import Column, String, UUID
from sqlalchemy.orm import relationship

from app.models.model_base import BaseModel as Base

class Media(Base):
    __tablename__ = 'media'
    
    media_id = Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True, default=uuid.uuid4)
    media_name = Column(String(128))
    media_type = Column(String(50))
    content_url = Column(String(128))

    # properties_units = relationship(
    #     'PropertyUnitAssoc',
    #     secondary='entity_media',
    #     primaryjoin="EntityMedia.media_id==Media.media_id",
    #     secondaryjoin="and_(EntityMedia.entity_id==PropertyUnitAssoc.property_unit_assoc_id, EntityMedia.entity_type=='Amenities')",
    #     back_populates="media_ammenities",
    #     overlaps="entity_media,media",
    #     lazy="selectin"
    # )
    # entity_media = relationship('EntityMedia', overlaps="entity_amenities,property_unit_assoc_id", back_populates='media')