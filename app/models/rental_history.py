import uuid
from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, UUID, String, ForeignKey

from app.models.model_base import BaseModel as Base


class PastRentalHistory(Base):
    __tablename__ = "past_rental_history"

    rental_history_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4,
    )
    address_hash = Column(UUID(as_uuid=True))
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    property_owner_name = Column(String, nullable=False)
    property_owner_email = Column(String, nullable=False)
    property_owner_mobile = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)

    user = relationship("User", back_populates="rental_histories")

    addresses = relationship(
        "Addresses",
        secondary="entity_address",
        primaryjoin="and_(PastRentalHistory.address_hash==EntityAddress.entity_id, EntityAddress.entity_type=='PastRentalHistory')",
        secondaryjoin="EntityAddress.address_id==Addresses.address_id",
        overlaps="address,entity_addresses,addresses,properties,users",
        back_populates="rental_history",
        lazy="selectin",
    )
