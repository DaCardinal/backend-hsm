from enum import Enum
from uuid import UUID
from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, Field

from app.models import CalendarEvent as CalendarEventModel
from app.schema import UserBase, Property, PropertyUnit, PropertyUnitAssoc

class EventTypeEnum(str, Enum):
    inspection = "inspection"
    meeting = "meeting"
    other = "other"

class CalendarEventBase(BaseModel):
    title: str = Field(..., example="Team Meeting")
    description: Optional[str] = Field(None, example="Quarterly team meeting to discuss project progress")
    event_type: EventTypeEnum = EventTypeEnum.other
    event_start_date: Optional[datetime] = None
    event_end_date: Optional[datetime] = None
    property_unit_assoc_id: Optional[UUID | Property | PropertyUnit | Any] = None
    organizer_id: Optional[UUID | UserBase] = None

    class Config:
        from_attributes = True

class CalendarEventCreateSchema(BaseModel):
    title: str = Field(..., example="Team Meeting")
    description: Optional[str] = Field(None, example="Quarterly team meeting to discuss project progress")
    event_type: EventTypeEnum = EventTypeEnum.other
    event_start_date: Optional[datetime] = None
    event_end_date: Optional[datetime] = None
    property_unit_assoc_id: Optional[UUID] = None
    organizer_id: Optional[UUID | UserBase] = None

    class Config:
        from_attributes = True
        use_enum_values = True
        populate_by_name = True

class CalendarEventUpdateSchema(CalendarEventBase):
    event_id: Optional[str] = Field("", alias='event_id')
    id: Optional[UUID] = Field(None, alias='id')

    class Config:
        from_attributes = True
        use_enum_values = True
        populate_by_name = True

class CalendarEventResponse(BaseModel):
    id: Optional[UUID] = Field(None, alias='id')
    title: str
    description: Optional[str]
    event_type: EventTypeEnum = Field(EventTypeEnum.other, example="meeting")
    event_start_date: datetime
    event_end_date: datetime
    property_unit_assoc: Optional[UUID | Property | PropertyUnit | Any]
    organizer_id: Optional[UUID | UserBase]

    @classmethod
    def get_property_info(cls, property: Property):
        property : Property = property

        return Property(
            property_unit_assoc_id = property.property_unit_assoc_id,
            name = property.name,
            property_type = property.property_type.name,
            amount = property.amount,
            security_deposit = property.security_deposit,
            commission = property.commission,
            floor_space = property.floor_space,
            num_units = property.num_units,
            num_bathrooms = property.num_bathrooms,
            num_garages = property.num_garages,
            has_balconies = property.has_balconies,
            has_parking_space = property.has_parking_space,
            pets_allowed = property.pets_allowed,
            description = property.description,
            property_status = property.property_status,
        )
    
    @classmethod
    def get_property_unit_info(cls, property_unit: PropertyUnit):
        property_unit : PropertyUnit = property_unit

        return PropertyUnit(
            property_unit_assoc_id = property_unit.property_unit_assoc_id,
            property_unit_code = property_unit.property_unit_code,
            property_unit_floor_space = property_unit.property_unit_floor_space,
            property_unit_amount = property_unit.property_unit_amount,
            property_floor_id = property_unit.property_floor_id,
            property_unit_notes = property_unit.property_unit_notes,
            has_amenities = property_unit.has_amenities,
            property_id = property_unit.property_id,
            property_unit_security_deposit = property_unit.property_unit_security_deposit,
            property_unit_commission = property_unit.property_unit_commission
        )
    
    @classmethod
    def get_property_unit_assoc(cls, property_unit_assoc: PropertyUnitAssoc):

        if property_unit_assoc.property_unit_type == "Units":
            property_unit_assoc = cls.get_property_unit_info(property_unit_assoc)
        else:
            property_unit_assoc = cls.get_property_info(property_unit_assoc)
            
        return property_unit_assoc

    @classmethod
    def from_orm_model(cls, calendar_event: CalendarEventModel):

        result = cls(
            id=calendar_event.id,
            event_id=calendar_event.event_id,
            title=calendar_event.title,
            description=calendar_event.description,
            event_type=calendar_event.event_type,
            event_start_date=calendar_event.event_start_date,
            event_end_date=calendar_event.event_end_date,
            property_unit_assoc=cls.get_property_unit_assoc(calendar_event.prop_assoc),
            organizer_id=calendar_event.organizer
        ).model_dump()

        return result