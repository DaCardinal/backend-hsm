from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Dict, Any, List, Optional, Union

# schemas
from app.schema.media import Media, MediaBase
from app.schema.billable import Billable
from app.schema.property_assignment import AssignmentType
from app.schema.amenity import Amenities, AmenitiesCreateSchema

# schemas mixins
from app.schema.mixins.billable_mixin import UtilitiesMixin
from app.schema.mixins.amenities_mixin import AmenitiesInfoMixin
from app.schema.mixins.user_mixins import UserBase, UserBaseMixin
from app.schema.mixins.address_mixin import AddressBase, Address, AddressMixin
from app.schema.mixins.property_mixin import (
    Property,
    PropertyBase,
    PropertyUnit,
    PropertyUnitBase,
    PropertyDetailsMixin,
)

# models
from app.models.unit import Units as UnitsModel
from app.models.property import Property as PropertyModel
from app.models.property_assignment import PropertyAssignment as PropertyAssignmentModel


class PropertyCreateSchema(PropertyBase):
    """
    Schema for creating a new property.

    Attributes:
        address (Optional[AddressBase]): The address of the property.
        media (Optional[List[Media] | List[MediaBase] | Media | MediaBase]): Media associated with the property.
        amenities (Optional[List[AmenitiesCreateSchema] | AmenitiesCreateSchema]): Amenities associated with the property.
        utilities (Optional[List[Billable] | Billable]): Utilities associated with the property.
    """

    address: Optional[AddressBase] = None
    media: Optional[List[Media] | List[MediaBase] | Media | MediaBase] = None
    amenities: Optional[List[AmenitiesCreateSchema] | AmenitiesCreateSchema] = None
    utilities: Optional[List[Billable] | Billable] = None

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class PropertyUpdateSchema(PropertyBase):
    """
    Schema for updating an existing property.

    Attributes:
        address (Optional[Address]): The address of the property.
        media (Optional[List[Media] | Media]): Media associated with the property.
        amenities (Optional[List[Amenities] | Amenities]): Amenities associated with the property.
        utilities (Optional[List[Billable] | Billable]): Utilities associated with the property.
    """

    address: Optional[Address] = None
    media: Optional[List[Media] | Media] = None
    amenities: Optional[List[Amenities] | Amenities] = None
    utilities: Optional[List[Billable] | Billable] = None

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class PropertyUnitCreateSchema(PropertyUnitBase):
    """
    Schema for creating a property unit.

    Attributes:
        media (Optional[List[Media] | List[MediaBase] | Media | MediaBase]): Media associated with the property unit.
        amenities (Optional[List[AmenitiesCreateSchema] | AmenitiesCreateSchema]): Amenities associated with the property unit.
        utilities (Optional[List[Billable] | Billable]): Utilities associated with the property unit.
    """

    media: Optional[List[Media] | List[MediaBase] | Media | MediaBase] = None
    amenities: Optional[List[AmenitiesCreateSchema] | AmenitiesCreateSchema] = None
    utilities: Optional[List[Billable] | Billable] = None

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class PropertyUnitUpdateSchema(PropertyUnit):
    """
    Schema for updating a property unit.

    Attributes:
        media (Optional[List[Media] | Media]): Media associated with the property unit.
        amenities (Optional[List[Amenities] | Amenities]): Amenities associated with the property unit.
        utilities (Optional[List[Billable] | Billable]): Utilities associated with the property unit.
    """

    media: Optional[List[Media] | Media] = None
    amenities: Optional[List[Amenities] | Amenities] = None
    utilities: Optional[List[Billable] | Billable] = None

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class PropertyUnitResponse(
    PropertyUnit, AmenitiesInfoMixin, UserBaseMixin, UtilitiesMixin
):
    """
    Model for representing a property unit response.

    Attributes:
        media (Optional[List[Media] | Media]): Media associated with the property unit.
        property (Optional[PropertyBase]): The property associated with the unit.
        amenities (Optional[List[Amenities] | Amenities]): Amenities associated with the property unit.
        utilities (Optional[List[Any]]): Utilities associated with the property unit.
    """

    media: Optional[List[Media] | Media] = None
    property: Optional[PropertyBase] = None
    amenities: Optional[List[Amenities] | Amenities] = None
    utilities: Optional[List[Any]] = None
    is_available: Optional[bool] = False
    assigned_users: Optional[List[Dict[str, Union[UserBase, AssignmentType]]]] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    @classmethod
    def from_orm_model(cls, property_unit: UnitsModel) -> "PropertyUnitResponse":
        """
        Create a PropertyUnitResponse instance from an ORM model.

        Args:
            property_unit (UnitsModel): Property unit ORM model.

        Returns:
            PropertyUnitResponse: Property unit response object.
        """
        return cls(
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
            property=property_unit.property,
            property_status=property_unit.property_status,
            media=property_unit.media,
            amenities=cls.get_amenities(property_unit.entity_amenities),
            utilities=cls.get_utilities_info(property_unit.utilities),
            assigned_users=cls.get_assigned_users(property_unit.assigned_users),
            is_available=property_unit.is_contract_active,
            created_at=property_unit.created_at,
        ).model_dump()


class PropertyResponse(
    Property, UserBaseMixin, AmenitiesInfoMixin, AddressMixin, UtilitiesMixin
):
    """
    Model for representing a property response.

    Attributes:
        units (Optional[List[PropertyUnit] | PropertyUnit]): The units associated with the property.
        media (Optional[List[Media] | Media]): Media associated with the property.
        amenities (Optional[List[Amenities] | Amenities]): Amenities associated with the property.
        utilities (Optional[List[Any]]): Utilities associated with the property.
    """

    units: Optional[List[PropertyUnit] | PropertyUnit] = None
    media: Optional[List[Media] | Media] = None
    amenities: Optional[List[Amenities] | Amenities] = None
    utilities: Optional[List[Any]] = None
    is_available: Optional[bool] = False
    assigned_users: Optional[List[Dict[str, Union[UserBase, AssignmentType]]]] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    @classmethod
    def from_orm_model(cls, property: PropertyModel) -> "PropertyResponse":
        """
        Create a PropertyResponse instance from an ORM model.

        Args:
            property (PropertyModel): Property ORM model.

        Returns:
            PropertyResponse: Property response object.
        """
        return cls(
            name=property.name,
            property_type=property.property_type,
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
            property_unit_assoc_id=property.property_unit_assoc_id,
            address=cls.get_address_base(property.addresses),
            units=property.units,
            media=property.media,
            amenities=cls.get_amenities(property.entity_amenities),
            utilities=cls.get_utilities_info(property.utilities),
            assigned_users=cls.get_assigned_users(property.assigned_users),
            is_available=property.is_contract_active,
            created_at=property.created_at,
        ).model_dump()


class PropertyAssignmentResponse(BaseModel, UserBaseMixin, PropertyDetailsMixin):
    """
    Schema for responding with PropertyAssignment data.

    Attributes:
        property_assignment_id (UUID): The unique identifier for the property assignment.
        property_unit_assoc_id (UUID): The UUID of the associated property unit.
        user_id (UUID): The UUID of the user assigned to the property.
        assignment_type (AssignmentType): The type of assignment.
        date_from (datetime): The start date of the assignment.
        date_to (Optional[datetime]): The optional end date of the assignment.
        notes (Optional[str]): Additional notes about the assignment.
    """

    property_assignment_id: UUID = None
    property_unit_assoc_id: Optional[Union[Property | PropertyUnit | Any]] = None
    user_id: Optional[UserBase] = None
    assignment_type: AssignmentType
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    @classmethod
    def from_orm_model(
        cls, assignment: PropertyAssignmentModel
    ) -> "PropertyAssignmentResponse":
        """
        Creates an instance of PropertyAssignmentResponse from an ORM model instance.

        Args:
            assignment (PropertyAssignment): The ORM model instance of PropertyAssignment.

        Returns:
            PropertyAssignmentResponse: The created instance of PropertyAssignmentResponse.
        """

        return cls(
            property_assignment_id=assignment.property_assignment_id,
            property_unit_assoc_id=cls.get_property_details(
                assignment.property_unit_assoc
            ),
            user_id=cls.get_user_info(assignment.user),
            assignment_type=assignment.assignment_type,
            date_from=assignment.date_from,
            date_to=assignment.date_to,
            notes=assignment.notes,
        )
