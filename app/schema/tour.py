from uuid import UUID
from datetime import datetime
from typing import Any, Optional, Union, Annotated
from pydantic import BaseModel, ConfigDict, EmailStr, constr

# models
from app.models.tour_bookings import Tour as TourModel
from app.models.user import User as UserModel

# schemas
from app.schema.user import UserBase
from app.schema.enums import TourStatus, TourType

# mixins
from app.schema.mixins.property_mixin import Property, PropertyUnit, PropertyUnitAssoc


class TourBookingBase(BaseModel):
    """
    Base model for tour booking information.

    Attributes:
        name (str): The name of the person booking the tour.
        email (EmailStr): The email address of the person booking the tour.
        phone_number (str): The phone number of the person booking the tour.
        tour_type (Optional[TourType]): The type of the tour.
        status (Optional[TourStatus]): The status of the tour.
        tour_date (datetime): The date of the tour.
        property_unit_assoc_id (Optional[Union[UUID, Property, PropertyUnit, Any]]): The associated property unit.
        user_id (Optional[Union[UUID, UserBase]]): The unique identifier of the user.
    """

    name: Annotated[str, constr(max_length=255)]
    email: EmailStr
    phone_number: Annotated[str, constr(max_length=20)]
    tour_type: Optional[TourType] = TourType.in_person
    status: Optional[TourStatus] = TourStatus.incoming
    tour_date: datetime
    property_unit_assoc_id: Optional[Union[UUID, Property, PropertyUnit, Any]] = None
    user_id: Optional[Union[UUID, UserBase]] = None

    model_config = ConfigDict(from_attributes=True)


class TourBooking(BaseModel):
    """
    Model for representing a tour booking with additional details.

    Attributes:
        tour_booking_id (Optional[UUID]): The unique identifier for the tour booking.
        name (str): The name of the person booking the tour.
        email (EmailStr): The email address of the person booking the tour.
        phone_number (str): The phone number of the person booking the tour.
        tour_type (Optional[TourType]): The type of the tour.
        status (Optional[TourStatus]): The status of the tour.
        tour_date (datetime): The date of the tour.
        property_unit_assoc_id (Optional[Union[UUID, Property, PropertyUnit, Any]]): The associated property unit.
        user (Optional[Union[UUID, UserBase]]): The unique identifier of the user.
    """

    tour_booking_id: Optional[UUID]
    name: Annotated[str, constr(max_length=255)]
    email: EmailStr
    phone_number: Annotated[str, constr(max_length=20)]
    tour_type: Optional[TourType] = TourType.in_person
    status: Optional[TourStatus] = TourStatus.incoming
    tour_date: datetime
    property_unit_assoc_id: Optional[Union[UUID, Property, PropertyUnit, Any]] = None
    user: Optional[Union[UUID, UserBase]] = None

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        use_enum_values=True,
    )


class Tour(TourBookingBase):
    """
    Model for representing a tour with additional details.

    Attributes:
        tour_booking_id (Optional[UUID]): The unique identifier for the tour booking.
    """

    tour_booking_id: Optional[UUID]

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        use_enum_values=True,
    )


class TourCreateSchema(TourBookingBase):
    """
    Schema for creating a tour.

    Inherits from TourBookingBase.
    """

    model_config = ConfigDict(from_attributes=True)


class TourUpdateSchema(TourBookingBase):
    """
    Schema for updating a tour.

    Inherits from TourBookingBase.
    """

    model_config = ConfigDict(from_attributes=True)


class TourResponse(BaseModel):
    """
    Model for representing a tour response.

    Attributes:
        tour_booking_id (Optional[UUID]): The unique identifier for the tour booking.
        email (str): The email address of the person booking the tour.
        name (str): The name of the person booking the tour.
        phone_number (str): The phone number of the person booking the tour.
        tour_type (Optional[TourType]): The type of the tour.
        status (Optional[TourStatus]): The status of the tour.
        tour_date (datetime): The date of the tour.
        property_unit_assoc (Optional[Union[UUID, Property, PropertyUnit, Any]]): The associated property unit.
        user (Optional[Union[UUID, UserBase]]): The unique identifier of the user.
    """

    tour_booking_id: Optional[UUID] = None
    email: EmailStr
    name: Annotated[str, constr(max_length=255)]
    phone_number: Annotated[str, constr(max_length=20)]
    tour_type: Optional[TourType] = TourType.in_person
    status: Optional[TourStatus] = TourStatus.incoming
    tour_date: datetime
    property_unit_assoc: Optional[Union[UUID, Property, PropertyUnit, Any]] = None
    user: Optional[Union[UUID, UserBase]] = None

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        use_enum_values=True,
        populate_by_name=True,
    )

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
            property_unit_commission=property_unit.property_unit_commission,
        )

    @classmethod
    def get_property_unit_assoc(
        cls, property_unit_assoc: PropertyUnitAssoc
    ) -> Union[Property, PropertyUnit, dict]:
        """
        Get detailed property unit association information.

        Args:
            property_unit_assoc (PropertyUnitAssoc): Property unit association object.

        Returns:
            Union[Property, PropertyUnit, dict]: Detailed property unit association object.
        """
        if property_unit_assoc is None:
            return {}

        if property_unit_assoc.property_unit_type == "Units":
            return cls.get_property_unit_info(property_unit_assoc)
        else:
            return cls.get_property_info(property_unit_assoc)

    @classmethod
    def get_user_info(cls, user: UserModel) -> UserBase:
        """
        Get basic user information.

        Args:
            user (UserModel): User ORM model.

        Returns:
            UserBase: Basic user information.
        """
        return UserBase(
            first_name=user.first_name,
            last_name=user.last_name,
            photo_url=user.photo_url,
            email=user.email,
        )

    @classmethod
    def from_orm_model(cls, tour_booking: TourModel) -> "TourResponse":
        """
        Create a TourResponse instance from an ORM model.

        Args:
            tour_booking (TourModel): Tour booking ORM model.

        Returns:
            TourResponse: Tour response object.
        """
        return cls(
            tour_booking_id=tour_booking.tour_booking_id,
            name=tour_booking.name,
            email=tour_booking.email,
            tour_type=tour_booking.tour_type,
            phone_number=tour_booking.phone_number,
            tour_date=tour_booking.tour_date,
            status=tour_booking.status,
            property_unit_assoc=cls.get_property_unit_assoc(
                tour_booking.property_unit_assoc
            ),
            user=tour_booking.user,
        ).model_dump()
