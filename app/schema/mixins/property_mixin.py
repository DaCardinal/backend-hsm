from uuid import UUID
from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Union

# schemas
from app.schema.mixins.address_mixin import Address

# enums
from app.schema.enums import PropertyType, PropertyStatus

# models
from app.models.contract import Contract as ContractModel
from app.models.property_unit_assoc import PropertyUnitAssoc as PropertyUnitAssocModel


class PropertyUnitAssoc(BaseModel):
    """
    Model for representing an association between property units.

    Attributes:
        property_unit_assoc_id (Optional[UUID]): The unique identifier for the property unit association.
        property_unit_type (Optional[str]): The type of the property unit.
    """

    property_unit_assoc_id: Optional[UUID] = None
    property_unit_type: Optional[str] = None

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


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

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class Property(PropertyBase):
    """
    Model for representing a property with additional details.

    Attributes:
        property_unit_assoc_id (Optional[UUID]): The unique identifier for the property unit association.
        address (Optional[List[Address] | Address]): The address(es) associated with the property.
    """

    property_unit_assoc_id: Optional[UUID]
    address: Optional[List[Address] | Address] = None

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class PropertyInfoMixin:
    @classmethod
    def get_property_info(cls, property: Property) -> Property:
        return Property(
            property_unit_assoc_id=property.property_unit_assoc_id,
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
        )


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
    property_status: PropertyStatus
    property_unit_notes: Optional[str] = None
    property_unit_security_deposit: Optional[float] = None
    property_unit_commission: Optional[float] = None
    has_amenities: Optional[bool] = False

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class PropertyUnit(PropertyUnitBase):
    """
    Model for representing a property unit with additional details.

    Attributes:
        property_unit_assoc_id (Optional[UUID]): The unique identifier for the property unit association.
    """

    property_unit_assoc_id: Optional[UUID]

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class PropertyUnitInfoMixin:
    @classmethod
    def get_property_unit_info(cls, property_unit: PropertyUnit) -> PropertyUnit:
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
            property_status=property_unit.property_status,
        )


class PropertyDetailsMixin(PropertyInfoMixin, PropertyUnitInfoMixin):
    PROPERTY_TYPE_DEFAULT = "Units"

    @classmethod
    def get_property_details_from_contract(cls, contract_details: List[ContractModel]):
        """
        Extract and format property details from a list of contract models.

        This method iterates over the provided contract models, extracting and converting
        property unit associations to their corresponding details based on their type (either
        'Units' or other types).

        Args:
            contract_details (List[ContractModel]): A list of contract models from which property
            details are extracted.
        """
        result = []

        for contract in contract_details:
            result.append(cls.get_property_details(contract.properties))

        return result

    @classmethod
    def get_property_details(
        cls,
        property_unit_assoc_details: Union[
            PropertyUnitAssocModel | List[PropertyUnitAssocModel]
        ],
    ) -> List[Union[Property, PropertyUnit]]:
        result = []

        # ensure it is a list
        property_unit_assoc_details = (
            [property_unit_assoc_details]
            if not isinstance(property_unit_assoc_details, list)
            else property_unit_assoc_details
        )

        for property_unit_assoc in property_unit_assoc_details:
            # TODO: prevent when property hasn't been linked to maintenance request
            if not property_unit_assoc:
                continue
            if (
                property_unit_assoc.property_unit_type
                == PropertyDetailsMixin.PROPERTY_TYPE_DEFAULT
            ):
                result.append(cls.get_property_unit_info(property_unit_assoc))
            else:
                result.append(cls.get_property_info(property_unit_assoc))
        return result
