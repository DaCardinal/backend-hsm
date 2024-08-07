import uuid
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Boolean, Integer, String, UUID

from app.models.model_base import BaseModel as Base


# TODO: Add to next update on message model
class ReminderFrequency(Base):
    __tablename__ = "reminder_frequency"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(50))
    frequency = Column(Integer)
    is_active = Column(Boolean, default=False)

    messages = relationship("Message", back_populates="reminder_frequency")
