from uuid import UUID
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

# schemas
from app.schema.media import Media, MediaBase
# from app.schema.payment_type import PaymentType
from app.schema.enums import PropertyType, PropertyStatus
from app.schema.amenity import Amenities, AmenitiesCreateSchema
from app.schema.address import Address, AddressBase, City, Region, Country
from app.schema.billable import Utilities, EntityBillable, EntityBillableCreate

# models
from app.models.unit import Units as UnitsModel
from app.models.address import Addresses as AddressModel
from app.models.property import Property as PropertyModel
from app.models.payment_type import PaymentTypes as PaymentTypeModel
from app.models.entity_billable import EntityBillable as EntityBillableModel
from app.models.entity_amenities import EntityAmenities as EntityAmenitiesModel

# models 
# EntityAmenitiesModel, AddressModel, EntityBillableModel, PaymentTypeModel, PropertyModel

# schemas
# Utilities | Done
# Media, MediaBase | Done
# Amenities, AmenitiesCreateSchema | Done
# EntityBillableCreate, EntityBillable | Done

class PropertyBase(BaseModel):
    """
    Base model for property information.

    Attributes:
        name (str): The name of the property.
        property_type (PropertyType): The type of the property.
        amount (float): The amount associated with the property.
        security_deposit (Optional[float]): The security deposit for the property.
        commission (Optional[float]): The commission for the property.
        floor_space (Optional[float]): The floor space of the property.
        num_units (Optional[int]): The number of units in the property.
        num_bathrooms (Optional[int]): The number of bathrooms in the property.
        num_garages (Optional[int]): The number of garages in the property.
        has_balconies (Optional[bool]): Indicates if the property has balconies.
        has_parking_space (Optional[bool]): Indicates if the property has parking space.
        pets_allowed (bool): Indicates if pets are allowed in the property.
        description (Optional[str]): The description of the property.
        property_status (PropertyStatus): The status of the property.
    """
    name: str
    property_type: PropertyType
    amount: float
    security_deposit: Optional[float] = None
    commission: Optional[float] = None
    floor_space: Optional[float] = None
    num_units: Optional[int] = None
    num_bathrooms: Optional[int] = None
    num_garages: Optional[int] = None
    has_balconies: Optional[bool] = False
    has_parking_space: Optional[bool] = False
    pets_allowed: bool = False
    description: Optional[str] = None
    property_status: PropertyStatus

    class Config:
        from_attributes = True
        use_enum_values = True


class Property(PropertyBase):
    """
    Model for representing a property with additional details.

    Attributes:
        property_unit_assoc_id (Optional[UUID]): The unique identifier for the property unit association.
        address (Optional[List[Address] | Address]): The address(es) associated with the property.
    """
    property_unit_assoc_id: Optional[UUID]
    address: Optional[List[Address] | Address] = None

    class Config:
        from_attributes = True
        use_enum_values = True


class PropertyCreateSchema(PropertyBase):
    """
    Schema for creating a new property.

    Attributes:
        address (Optional[AddressBase]): The address of the property.
        media (Optional[List[Media] | List[MediaBase] | Media | MediaBase]): Media associated with the property.
        amenities (Optional[List[AmenitiesCreateSchema] | AmenitiesCreateSchema]): Amenities associated with the property.
        utilities (Optional[List[EntityBillableCreate] | EntityBillableCreate]): Utilities associated with the property.
    """
    address: Optional[AddressBase] = None
    media: Optional[List[Media] | List[MediaBase] | Media | MediaBase] = None
    amenities: Optional[List[AmenitiesCreateSchema] | AmenitiesCreateSchema] = None
    utilities: Optional[List[EntityBillableCreate] | EntityBillableCreate] = None

    class Config:
        from_attributes = True
        use_enum_values = True


class PropertyUpdateSchema(PropertyBase):
    """
    Schema for updating an existing property.

    Attributes:
        address (Optional[Address]): The address of the property.
        media (Optional[List[Media] | Media]): Media associated with the property.
        amenities (Optional[List[Amenities] | Amenities]): Amenities associated with the property.
        utilities (Optional[List[EntityBillableCreate] | EntityBillableCreate]): Utilities associated with the property.
    """
    address: Optional[Address] = None
    media: Optional[List[Media] | Media] = None
    amenities: Optional[List[Amenities] | Amenities] = None
    utilities: Optional[List[EntityBillableCreate] | EntityBillableCreate] = None

    class Config:
        from_attributes = True
        use_enum_values = True


class PropertyUnitBase(BaseModel):
    """
    Base model for property unit information.

    Attributes:
        property_id (UUID): The unique identifier for the property.
        property_unit_code (Optional[str]): The code of the property unit.
        property_unit_floor_space (Optional[int]): The floor space of the property unit.
        property_unit_amount (Optional[float]): The amount associated with the property unit.
        property_floor_id (Optional[int]): The floor ID of the property unit.
        property_unit_notes (Optional[str]): The notes for the property unit.
        property_unit_security_deposit (Optional[float]): The security deposit for the property unit.
        property_unit_commission (Optional[float]): The commission for the property unit.
        has_amenities (Optional[bool]): Indicates if the property unit has amenities.
    """
    property_id: UUID
    property_unit_code: Optional[str] = None
    property_unit_floor_space: Optional[int] = None
    property_unit_amount: Optional[float] = None
    property_floor_id: Optional[int] = None
    property_unit_notes: Optional[str] = None
    property_unit_security_deposit: Optional[float] = None
    property_unit_commission: Optional[float] = None
    has_amenities: Optional[bool] = False

    class Config:
        from_attributes = True
        use_enum_values = True


class PropertyUnit(PropertyUnitBase):
    """
    Model for representing a property unit with additional details.

    Attributes:
        property_unit_assoc_id (Optional[UUID]): The unique identifier for the property unit association.
    """
    property_unit_assoc_id: Optional[UUID]

    class Config:
        from_attributes = True
        use_enum_values = True


class PropertyUnitCreateSchema(PropertyUnitBase):
    """
    Schema for creating a property unit.

    Attributes:
        media (Optional[List[Media] | List[MediaBase] | Media | MediaBase]): Media associated with the property unit.
        amenities (Optional[List[AmenitiesCreateSchema] | AmenitiesCreateSchema]): Amenities associated with the property unit.
        utilities (Optional[List[EntityBillableCreate] | EntityBillableCreate]): Utilities associated with the property unit.
    """
    media: Optional[List[Media] | List[MediaBase] | Media | MediaBase] = None
    amenities: Optional[List[AmenitiesCreateSchema] | AmenitiesCreateSchema] = None
    utilities: Optional[List[EntityBillableCreate] | EntityBillableCreate] = None

    class Config:
        from_attributes = True
        use_enum_values = True


class PropertyUnitUpdateSchema(PropertyUnit):
    """
    Schema for updating a property unit.

    Attributes:
        media (Optional[List[Media] | Media]): Media associated with the property unit.
        amenities (Optional[List[Amenities] | Amenities]): Amenities associated with the property unit.
        utilities (Optional[List[EntityBillableCreate] | EntityBillableCreate]): Utilities associated with the property unit.
    """
    media: Optional[List[Media] | Media] = None
    amenities: Optional[List[Amenities] | Amenities] = None
    utilities: Optional[List[EntityBillableCreate] | EntityBillableCreate] = None

    class Config:
        from_attributes = True
        use_enum_values = True


class PropertyUnitAssoc(BaseModel):
    """
    Model for representing an association between property units.

    Attributes:
        property_unit_assoc_id (Optional[UUID]): The unique identifier for the property unit association.
        property_unit_type (Optional[str]): The type of the property unit.
    """
    property_unit_assoc_id: Optional[UUID] = None
    property_unit_type: Optional[str] = None

    class Config:
        from_attributes = True
        use_enum_values = True


class PropertyUnitResponse(PropertyUnit):
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

    class Config:
        from_attributes = True
        use_enum_values = True

    @classmethod
    def get_amenities(cls, entity_amenities: List[EntityAmenitiesModel]) -> List[Amenities]:
        """
        Get amenities information.

        Args:
            entity_amenities (List[EntityAmenitiesModel]): List of entity amenities models.

        Returns:
            List[Amenities]: List of amenities.
        """
        result = []

        for entity_amenity in entity_amenities:
            amenities_info : List[Amenities] | Amenities = entity_amenity.amenity

            if not isinstance(amenities_info, list):
                amenities_info = [amenities_info]

            for amenity in amenities_info:

                result.append(Amenities(
                    amenity_id=amenity.amenity_id,
                    amenity_name=amenity.amenity_name,
                    amenity_short_name=amenity.amenity_short_name,
                    amenity_value_type=amenity.amenity_value_type,
                    description=amenity.description,
                    media=entity_amenity.media
                ))

        return result

    @classmethod
    def get_utilities_info(cls, utilities: List[EntityBillable]) -> List[Dict[str, Any]]:
        """
        Get utilities information.

        Args:
            utilities (List[EntityBillable]): List of entity billable objects.

        Returns:
            List[Dict[str, Any]]: List of utility information.
        """
        result = []

        for entity_utility in utilities:
            entity_utility : EntityBillableModel = entity_utility
            payment_type : PaymentTypeModel = entity_utility.payment_type
            utility : Utilities = entity_utility.utility

            # TODO: Return actuable entity billable pydantic object
            result.append({
                "utility": utility.name,
                "payment_type": payment_type.payment_type_name,
                "utility_value": entity_utility.billable_amount,
                "apply_to_units": False,
                "entity_utilities_id": entity_utility.billable_assoc_id
            })

        return result

    @classmethod
    def from_orm_model(cls, property_unit: UnitsModel) -> 'PropertyUnitResponse':
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
            media=property_unit.media,
            amenities=cls.get_amenities(property_unit.entity_amenities),
            utilities=cls.get_utilities_info(property_unit.utilities)
        ).model_dump()


class PropertyResponse(Property):
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

    class Config:
        from_attributes = True
        use_enum_values = True

    @classmethod
    def get_address_base(cls, addresses: List[AddressModel]) -> List[Address]:
        """
        Get base address information.

        Args:
            addresses (List[AddressModel]): List of address objects.

        Returns:
            List[Address]: List of address base objects.
        """
        result = []

        for addr in addresses:
            addr_city : City = addr.city
            addr_region : Region = addr.region
            addr_country : Country = addr.country

            result.append(Address(
                address_id=addr.address_id,
                address_type=addr.address_type,
                primary=addr.primary,
                address_1=addr.address_1,
                address_2=addr.address_2,
                address_postalcode=addr.address_postalcode,
                city = addr_city.city_name,
                region = addr_region.region_name,
                country = addr_country.country_name
            ))

        return result

    @classmethod
    def get_utilities_info(cls, utilities: List[EntityBillable]) -> List[Dict[str, Any]]:
        """
        Get utilities information.

        Args:
            utilities (List[EntityBillable]): List of entity billable objects.

        Returns:
            List[Dict[str, Any]]: List of utility information.
        """
        result = []

        for entity_utility in utilities:
            entity_utility : EntityBillableModel = entity_utility
            payment_type : PaymentTypeModel = entity_utility.payment_type
            utility : Utilities  = entity_utility.utility
            
            # TODO: Return actuable entity billable pydantic object
            result.append({
                "utility": utility.name,
                "payment_type": payment_type.payment_type_name,
                "utility_value": entity_utility.billable_amount,
                "apply_to_units": False,
                "entity_utilities_id": entity_utility.billable_assoc_id
            })

        return result

    @classmethod
    def get_amenities(cls, entity_amenities: List[EntityAmenitiesModel]) -> List[Amenities]:
        """
        Get amenities information.

        Args:
            entity_amenities (List[EntityAmenitiesModel]): List of entity amenities models.

        Returns:
            List[Amenities]: List of amenities.
        """
        result = []

        for entity_amenity in entity_amenities:
            amenities_info : List[Amenities] | Amenities = entity_amenity.amenity

            if not isinstance(amenities_info, list):
                amenities_info = [amenities_info]

            for amenity in amenities_info:

                result.append(Amenities(
                    amenity_id=amenity.amenity_id,
                    amenity_name=amenity.amenity_name,
                    amenity_short_name=amenity.amenity_short_name,
                    amenity_value_type=amenity.amenity_value_type,
                    description=amenity.description,
                    media=entity_amenity.media
                ))

        return result

    @classmethod
    def from_orm_model(cls, property: PropertyModel) -> 'PropertyResponse':
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
            utilities=cls.get_utilities_info(property.utilities)
        ).model_dump()
