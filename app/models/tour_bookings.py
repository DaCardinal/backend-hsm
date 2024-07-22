import enum
import uuid
from sqlalchemy import UUID, Column, String, Enum, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.models.model_base import BaseModel as Base


class TourType(str, enum.Enum):
    in_person = "in_person"
    video = "video_chat"


class TourStatus(str, enum.Enum):
    incoming = "incoming"
    completed = "completed"
    cancelled = "cancelled"


# TODO: Relationship for unit, property and tours
class Tour(Base):
    __tablename__ = "tour"

    tour_booking_id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String)
    email = Column(String)
    phone_number = Column(String)
    tour_type = Column(
        Enum(TourType), default=TourType.in_person, nullable=True, name="tour_type"
    )
    status = Column(
        Enum(TourStatus), default=TourStatus.incoming, nullable=True, name="status"
    )
    tour_date = Column(DateTime(timezone=True), default=func.now())
    property_unit_assoc_id = Column(
        UUID,
        ForeignKey("property_unit_assoc.property_unit_assoc_id", ondelete="CASCADE"),
    )
    user_id = Column(
        UUID, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=True
    )

    user = relationship("User", back_populates="tours", lazy="selectin")

    property = relationship(
        "Property",
        secondary="property_unit_assoc",
        primaryjoin="Tour.property_unit_assoc_id == PropertyUnitAssoc.property_unit_assoc_id",
        secondaryjoin="Property.property_unit_assoc_id == PropertyUnitAssoc.property_unit_assoc_id",
        viewonly=True,
        back_populates="tour_bookings",
        lazy="selectin",
    )

    unit = relationship(
        "Units",
        secondary="property_unit_assoc",
        primaryjoin="Tour.property_unit_assoc_id == PropertyUnitAssoc.property_unit_assoc_id",
        secondaryjoin="Units.property_unit_assoc_id == PropertyUnitAssoc.property_unit_assoc_id",
        viewonly=True,
        back_populates="tour_bookings",
        lazy="selectin",
    )

    property_unit_assoc = relationship(
        "PropertyUnitAssoc",
        back_populates="prop_unit_assoc_tours",
        cascade="save-update, merge",
        primaryjoin="Tour.property_unit_assoc_id == PropertyUnitAssoc.property_unit_assoc_id",
        overlaps="property,unit",
        foreign_keys=[property_unit_assoc_id],
        lazy="selectin",
        viewonly=True,
    )
