from sqlalchemy import Column, Boolean, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.model_base import BaseModel as Base


class ReminderFrequency(Base):
    __tablename__ = 'reminder_frequency'
    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(String(50))
    frequency = Column(Integer)
    is_active = Column(Boolean, default=False)

    # messages = relationship('Message', back_populates='reminder_frequency')