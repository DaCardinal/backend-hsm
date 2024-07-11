from pydantic import BaseModel, EmailStr
from typing import Any, Optional
from uuid import UUID
from datetime import datetime
from enum import Enum


from app.models import Tour as TourModel, User
from app.schema import UserBase, Property, PropertyUnit, PropertyUnitAssoc


class TourType(str, Enum):
    in_person = "in_person"
    virtual = "virtual"

class TourStatus(str, Enum):
    incoming = "incoming"
    completed = "completed"
    cancelled = "cancelled"

class TourBookingBase(BaseModel):
    name: str
    email: EmailStr
    phone_number: str
    tour_type: Optional[TourType] = TourType.in_person
    status: Optional[TourStatus] = TourStatus.incoming
    tour_date: datetime
    property_unit_assoc_id: Optional[UUID | Property | PropertyUnit | Any] = None
    user_id: Optional[UUID | UserBase] = None

    class Config:
        from_attributes = True


class TourBooking(BaseModel):
    tour_booking_id: Optional[UUID]
    name: str
    email: EmailStr
    phone_number: str
    tour_type: Optional[TourType] = TourType.in_person
    status: Optional[TourStatus] = TourStatus.incoming
    tour_date: datetime
    property_unit_assoc_id: Optional[UUID | Property | PropertyUnit | Any] = None
    user: Optional[UUID | UserBase] = None

    class Config:
        from_attributes = True
        use_enum_values = True
        populate_by_name = True

class Tour(TourBookingBase):
    tour_booking_id: Optional[UUID]

    class Config:
        from_attributes = True
        use_enum_values = True
        populate_by_name = True

class TourCreateSchema(TourBookingBase):
    class Config:
        from_attributes = True

class TourUpdateSchema(TourBookingBase):
    class Config:
        from_attributes = True

class TourResponse(BaseModel):
    tour_booking_id: Optional[UUID] = None
    email: str = None
    name: str = None
    phone_number: str = None
    tour_type: Optional[TourType] = TourType.in_person
    status: Optional[TourStatus] = TourStatus.incoming
    tour_date: datetime = None
    property_unit_assoc: Optional[UUID | Property | PropertyUnit | Any] = None
    user: Optional[UUID | UserBase] = None

    class Config:
        from_attributes = True
        use_enum_values = True
        populate_by_name = True
        arbitrary_types_allowed=True

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

        if property_unit_assoc is None:
            return {}
        
        if property_unit_assoc.property_unit_type == "Units":
            property_unit_assoc = cls.get_property_unit_info(property_unit_assoc)
        else:
            property_unit_assoc = cls.get_property_info(property_unit_assoc)
            
        return property_unit_assoc
    
    @classmethod
    def get_user_info(cls, user: User):
        print(user)

        return User(
            first_name=user.first_name,
            last_name=user.last_name,
            photo_url=user.photo_url,
            email=user.email
        )
        
    @classmethod
    def from_orm_model(cls, tour_booking: TourModel):

        result = cls(
            tour_booking_id = tour_booking.tour_booking_id,
            name = tour_booking.name,
            email = tour_booking.email,
            tour_type = tour_booking.tour_type.name,
            phone_number = tour_booking.phone_number,
            tour_date = tour_booking.tour_date,
            status = tour_booking.status.name,
            property_unit_assoc = cls.get_property_unit_assoc(tour_booking.property_unit_assoc),
            user = tour_booking.user
        ).model_dump()

        return result