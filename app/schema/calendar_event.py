from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict, constr
from typing import Optional, Union, Annotated

# schema
from app.schema.user import UserBase
from app.schema.enums import CalendarStatus, EventType

# models
from app.models.calendar_event import CalendarEvent as CalendarEventModel

# mixins


class CalendarEventBase(BaseModel):
    """
    Base model for calendar event information.

    Attributes:
        title (str): The title of the event.
        event_id (str): The unique identifier for the event.
        description (Optional[str]): The description of the event.
        event_type (EventTypeEnum): The type of the event.
        event_start_date (Optional[datetime]): The start date of the event.
        event_end_date (Optional[datetime]): The end date of the event.
        organizer_id (Optional[Union[UUID, UserBase]]): The unique identifier for the event organizer.
    """

    title: Annotated[str, constr(max_length=255)]
    event_id: Annotated[str, constr(max_length=50)]
    description: Optional[Annotated[str, constr(max_length=255)]] = None
    status: CalendarStatus = CalendarStatus.pending
    event_type: EventType = EventType.other
    event_start_date: Optional[datetime] = None
    event_end_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    organizer_id: Optional[Union[UUID, UserBase]] = None

    model_config = ConfigDict(from_attributes=True)


class CalendarEvent(CalendarEventBase):
    """
    Base model for calendar event information.

    Attributes:
        id (Optional[UUID]): The unique identifier for the maintenance request.
        title (str): The title of the event.
        event_id (str): The unique identifier for the event.
        description (Optional[str]): The description of the event.
        event_type (EventTypeEnum): The type of the event.
        event_start_date (Optional[datetime]): The start date of the event.
        event_end_date (Optional[datetime]): The end date of the event.
        organizer_id (Optional[Union[UUID, UserBase]]): The unique identifier for the event organizer.
    """

    id: Optional[UUID] = None
    title: Annotated[str, constr(max_length=255)]
    event_id: Annotated[str, constr(max_length=50)]
    description: Optional[Annotated[str, constr(max_length=255)]] = None
    status: CalendarStatus = CalendarStatus.pending
    event_type: EventType = EventType.other
    event_start_date: Optional[datetime] = None
    event_end_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    organizer_id: Optional[Union[UUID, UserBase]] = None

    model_config = ConfigDict(from_attributes=True)


class CalendarEventCreateSchema(BaseModel):
    """
    Schema for creating a calendar event.

    Attributes:
        title (str): The title of the event.
        description (Optional[str]): The description of the event.
        event_type (EventTypeEnum): The type of the event.
        event_start_date (Optional[datetime]): The start date of the event.
        event_end_date (Optional[datetime]): The end date of the event.
        organizer_id (Optional[Union[UUID, UserBase]]): The unique identifier for the event organizer.
    """

    title: Annotated[str, constr(max_length=255)]
    description: Optional[Annotated[str, constr(max_length=255)]] = None
    status: CalendarStatus = CalendarStatus.pending
    event_type: EventType = EventType.other
    event_start_date: Optional[datetime] = None
    event_end_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    organizer_id: Optional[Union[UUID, UserBase]] = None

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        use_enum_values=True,
    )


class CalendarEventUpdateSchema(BaseModel):
    """
    Schema for updating a calendar event.

    Attributes:
        event_id (Optional[str]): The unique identifier for the event.
        id (Optional[UUID]): The unique identifier for the event in the database.
        title (Optional[str]): The title of the event.
        description (Optional[str]): The description of the event.
        event_type (Optional[EventTypeEnum]): The type of the event.
        event_start_date (Optional[datetime]): The start date of the event.
        event_end_date (Optional[datetime]): The end date of the event.
        organizer_id (Optional[Union[UUID, UserBase]]): The unique identifier for the event organizer.
    """

    event_id: Optional[Annotated[str, constr(max_length=50)]] = None
    id: Optional[UUID] = None
    title: Optional[Annotated[str, constr(max_length=255)]] = None
    description: Optional[Annotated[str, constr(max_length=255)]] = None
    status: Optional[CalendarStatus]
    event_type: Optional[EventType]
    event_start_date: Optional[datetime] = None
    event_end_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    organizer_id: Optional[Union[UUID, UserBase]] = None

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        use_enum_values=True,
    )


class CalendarEventResponse(BaseModel):
    """
    Model for representing a calendar event response.

    Attributes:
        id (Optional[UUID]): The unique identifier for the event.
        event_id (str): The unique identifier for the event.
        title (str): The title of the event.
        description (Optional[str]): The description of the event.
        event_type (EventTypeEnum): The type of the event.
        event_start_date (datetime): The start date of the event.
        event_end_date (datetime): The end date of the event.
        organizer_id (Optional[Union[UUID, UserBase]]): The unique identifier for the event organizer.
    """

    id: Optional[UUID] = None
    event_id: Annotated[str, constr(max_length=50)]
    title: Annotated[str, constr(max_length=255)]
    description: Optional[Annotated[str, constr(max_length=255)]] = None
    event_type: EventType = EventType.other
    event_start_date: datetime
    event_end_date: datetime
    organizer_id: Optional[Union[UUID, UserBase]] = None

    @classmethod
    def from_orm_model(cls, calendar_event: CalendarEventModel):
        """
        Create a CalendarEventResponse instance from an ORM model.

        Args:
            calendar_event (CalendarEventModel): Calendar event ORM model.

        Returns:
            CalendarEventResponse: Calendar event response object.
        """
        return cls(
            id=calendar_event.id,
            event_id=calendar_event.event_id,
            title=calendar_event.title,
            description=calendar_event.description,
            event_type=calendar_event.event_type,
            event_start_date=calendar_event.event_start_date,
            event_end_date=calendar_event.event_end_date,
            organizer_id=calendar_event.organizer,
        )
