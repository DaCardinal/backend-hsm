from datetime import datetime
import pytz
from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, ForeignKey, Text, UUID

from app.models.model_base import BaseModel as Base


class UserInteractions(Base):
    __tablename__ = "user_interactions"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), primary_key=True)
    employee_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    property_unit_assoc_id = Column(
        UUID(as_uuid=True), ForeignKey("property_unit_assoc.property_unit_assoc_id")
    )
    contact_time = Column(
        DateTime(timezone=True), default=lambda: datetime.now(pytz.utc)
    )
    contact_details = Column(Text)

    user = relationship(
        "User", foreign_keys=[user_id], back_populates="interactions_as_user"
    )
    employee = relationship(
        "User", foreign_keys=[employee_id], back_populates="interactions_as_employee"
    )
