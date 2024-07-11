from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, constr
from typing import Optional, Union, Annotated

# schema
from app.schema.user import UserBase
from app.schema.enums import EventType
from app.schema.property import Property, PropertyUnit, PropertyUnitAssoc

# models
from app.models import CalendarEvent as CalendarEventModel


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
    event_type: EventType = EventType.other
    event_start_date: Optional[datetime] = None
    event_end_date: Optional[datetime] = None
    organizer_id: Optional[Union[UUID, UserBase]] = None

    class Config:
        from_attributes = True

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
    event_type: EventType = EventType.other
    event_start_date: Optional[datetime] = None
    event_end_date: Optional[datetime] = None
    organizer_id: Optional[Union[UUID, UserBase]] = None

    class Config:
        from_attributes = True


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
    event_type: EventType = EventType.other
    event_start_date: Optional[datetime] = None
    event_end_date: Optional[datetime] = None
    organizer_id: Optional[Union[UUID, UserBase]] = None

    class Config:
        from_attributes = True
        use_enum_values = True
        populate_by_name = True

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
    event_type: Optional[EventType] = None
    event_start_date: Optional[datetime] = None
    event_end_date: Optional[datetime] = None
    organizer_id: Optional[Union[UUID, UserBase]] = None

    class Config:
        from_attributes = True
        use_enum_values = True
        populate_by_name = True

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
    def get_property_info(cls, property: Property) -> Property:
        """
        Get detailed property information.

        Args:
            property (Property): Property object.

        Returns:
            Property: Detailed property object.
        """
        return Property(
            property_unit_assoc_id=property.property_unit_assoc_id,
            name=property.name,
            property_type=property.property_type.name,
            amount=property.amount,
            security_deposit=property.security_deposit,
            commission=property.commission,
            floor_space=property.floor_space,
            num_units=property.num_units,
            num_bathrooms=property.num_bathrooms,
            num_garages=property.num_garages,
            has_balconies=property.has_balconies,
            has_parking_space=property.has_parking_space,
            pets_allowed=property.pets_allowed,
            description=property.description,
            property_status=property.property_status,
        )
    
    @classmethod
    def get_property_unit_info(cls, property_unit: PropertyUnit) -> PropertyUnit:
        """
        Get detailed property unit information.

        Args:
            property_unit (PropertyUnit): Property unit object.

        Returns:
            PropertyUnit: Detailed property unit object.
        """
        return PropertyUnit(
            property_unit_assoc_id=property_unit.property_unit_assoc_id,
            property_unit_code=property_unit.property_unit_code,
            property_unit_floor_space=property_unit.property_unit_floor_space,
            property_unit_amount=property_unit.property_unit_amount,
            property_floor_id=property_unit.property_floor_id,
            property_unit_notes=property_unit.property_unit_notes,
            has_amenities=property_unit.has_amenities,
            property_id=property_unit.property_id,
            property_unit_security_deposit=property_unit.property_unit_security_deposit,
            property_unit_commission=property_unit.property_unit_commission
        )
    
    @classmethod
    def get_property_unit_assoc(cls, property_unit_assoc: PropertyUnitAssoc) -> Union[Property, PropertyUnit]:
        """
        Get detailed property unit association information.

        Args:
            property_unit_assoc (PropertyUnitAssoc): Property unit association object.

        Returns:
            Union[Property, PropertyUnit]: Detailed property unit association object.
        """
        if property_unit_assoc.property_unit_type == "Units":
            return cls.get_property_unit_info(property_unit_assoc)
        else:
            return cls.get_property_info(property_unit_assoc)

    @classmethod
    def from_orm_model(cls, calendar_event: CalendarEventModel) -> 'CalendarEventResponse':
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
            organizer_id=calendar_event.organizer
        ).model_dump()
