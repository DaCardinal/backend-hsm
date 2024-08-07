import enum
from datetime import datetime
import uuid
import pytz
from sqlalchemy.orm import relationship
from sqlalchemy import (
    event,
    Column,
    ForeignKey,
    DateTime,
    Enum,
    UUID,
    String,
    Text,
)

from app.models.model_base import BaseModel as Base


class CalendarStatusEnum(enum.Enum):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"


class EventTypeEnum(enum.Enum):
    inspection = "inspection"
    meeting = "meeting"
    other = "other"
    birthday = "birthday"
    holiday = "holiday"
    maintenance_request = "maintenance_request"


class CalendarEvent(Base):
    __tablename__ = "calendar_events"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4,
    )
    event_id = Column(String(128), unique=True, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(CalendarStatusEnum, default=CalendarStatusEnum.pending))
    event_type = Column(Enum(EventTypeEnum), default=EventTypeEnum.other, nullable=True)
    event_start_date = Column(
        DateTime(timezone=True), default=lambda: datetime.now(pytz.utc), nullable=True
    )
    event_end_date = Column(
        DateTime(timezone=True), default=lambda: datetime.now(pytz.utc), nullable=True
    )
    completed_date = Column(
        DateTime(timezone=True), default=lambda: datetime.now(pytz.utc), nullable=True
    )
    organizer_id = Column(
        UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False
    )

    organizer = relationship("User", back_populates="events", lazy="selectin")


@event.listens_for(CalendarEvent, "before_insert")
def receive_before_insert(mapper, connection, target: CalendarEvent):
    event: dict = target.to_dict()

    if "event_id" not in event or not event["event_id"]:
        current_time_str = datetime.now().strftime("%Y%m%d%H%M%S")
        setattr(target, "event_id", f"EV{current_time_str}")


@event.listens_for(CalendarEvent, "after_insert")
def receive_after_insert(mapper, connection, target: CalendarEvent):
    event: dict = target.to_dict()

    if "event_id" not in event or not event["event_id"] or not target.event_id:
        current_time_str = datetime.now().strftime("%Y%m%d%H%M%S")
        target.event_id = f"EV{current_time_str}"
        connection.execute(
            target.__table__.update()
            .where(target.__table__.c.id == target.id)
            .values(event_id=target.event_id)
        )
