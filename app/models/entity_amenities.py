import uuid
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Boolean, String, UUID

from app.models.model_base import BaseModel as Base


class EntityAmenities(Base):
    __tablename__ = "entity_amenities"

    entity_amenities_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4,
    )
    entity_type = Column(String)
    amenity_id = Column(UUID(as_uuid=True), ForeignKey("amenities.amenity_id"))
    entity_assoc_id = Column(
        UUID(as_uuid=True),
        ForeignKey("property_unit_assoc.property_unit_assoc_id", ondelete="CASCADE"),
    )
    apply_to_units = Column(Boolean, default=False)

    amenity = relationship("Amenities", overlaps="amenities", lazy="selectin")
    media = relationship(
        "Media",
        secondary="entity_media",
        primaryjoin="EntityAmenities.entity_amenities_id == EntityMedia.media_assoc_id",
        secondaryjoin="and_(EntityMedia.media_id == Media.media_id, EntityMedia.entity_type == 'EntityAmenities')",
        lazy="selectin",
    )
