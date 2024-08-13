import uuid
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Boolean, String, UUID

from app.models.model_base import BaseModel as Base


class EntityAddress(Base):
    __tablename__ = "entity_address"

    entity_assoc_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_type = Column(String(80))
    entity_id = Column(UUID(as_uuid=True))
    address_id = Column(UUID(as_uuid=True), ForeignKey("addresses.address_id"))
    emergency_address = Column(Boolean, default=False, nullable=True)
    emergency_address_hash = Column(String(128), default="", nullable=True)

    address = relationship(
        "Addresses",
        back_populates="entity_addresses",
        overlaps="users,properties,rental_history",
    )
