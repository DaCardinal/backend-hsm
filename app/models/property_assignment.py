from datetime import datetime
import enum
import uuid
import pytz
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    ForeignKey,
    DateTime,
    Enum,
    Text,
    UUID,
)

from app.models.model_base import BaseModel as Base


class AssignmentType(enum.Enum):
    other = "other"
    handler = "handler"
    landlord = "landlord"
    contractor = "contractor"


class PropertyAssignment(Base):
    __tablename__ = "property_assignment"

    property_assignment_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4,
    )
    property_unit_assoc_id = Column(
        UUID(as_uuid=True), ForeignKey("property_unit_assoc.property_unit_assoc_id")
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    assignment_type = Column(Enum(AssignmentType))
    date_from = Column(DateTime(timezone=True), default=lambda: datetime.now(pytz.utc))
    date_to = Column(DateTime(timezone=True), default=lambda: datetime.now(pytz.utc))
    notes = Column(Text)

    property_unit_assoc = relationship(
        "PropertyUnitAssoc", lazy="selectin", viewonly=True
    )
    user = relationship("User", lazy="selectin", viewonly=True)
