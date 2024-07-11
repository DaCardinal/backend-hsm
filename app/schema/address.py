from uuid import UUID, uuid4
from pydantic import BaseModel, constr
from typing import Annotated, Any, Optional

# local imports
from app.schema.enums import AddressTypeEnum

class City(BaseModel):
    """
    Model for representing a city.

    Attributes:
        city_id (UUID): The unique identifier for the city, defaults to a new UUID.
        region_id (UUID): The unique identifier for the associated region.
        city_name (str): The name of the city, with a maximum length of 128 characters.
    """
    city_id: Annotated[UUID, uuid4()] = uuid4()
    region_id: UUID
    city_name: Annotated[str, constr(max_length=128)]

    class Config:
        from_attributes = True


class Region(BaseModel):
    """
    Model for representing a region.

    Attributes:
        region_id (UUID): The unique identifier for the region, defaults to a new UUID.
        country_id (UUID): The unique identifier for the associated country.
        region_name (str): The name of the region, with a maximum length of 128 characters.
    """
    region_id: Annotated[UUID, uuid4()] = uuid4()
    country_id: UUID
    region_name: Annotated[str, constr(max_length=128)]

    class Config:
        from_attributes = True


class Country(BaseModel):
    """
    Model for representing a country.

    Attributes:
        country_id (UUID): The unique identifier for the country, defaults to a new UUID.
        country_name (str): The name of the country, with a maximum length of 128 characters.
    """
    country_id: Annotated[UUID, uuid4()] = uuid4()
    country_name: Annotated[str, constr(max_length=128)]

    class Config:
        from_attributes = True


# Ensure pydantic schema is initialized TODO: Remove
City.model_rebuild()
Region.model_rebuild()
Country.model_rebuild()


class AddressBase(BaseModel):
    """
    Base model for representing an address.

    Attributes:
        address_type (AddressTypeEnum): The type of the address.
        primary (Optional[bool]): Indicates if this is the primary address, defaults to True.
        address_1 (Optional[str]): The first line of the address.
        address_2 (Optional[str]): The second line of the address, defaults to None.
        city (str|UUID|Any): The city name or identifier.
        region (str|UUID|Any): The region name or identifier.
        country (str|UUID|Any): The country name or identifier.
        address_postalcode (Optional[str]): The postal code of the address.
    """
    address_type: AddressTypeEnum
    primary: Optional[bool] = True
    address_1: Optional[str]
    address_2: Optional[str] = None
    city: str | UUID | Any
    region: str | UUID | Any
    country: str | UUID | Any
    address_postalcode: Optional[str]

    class Config:
        from_attributes = True


class Address(AddressBase):
    """
    Model for representing an address with an optional address ID.

    Attributes:
        address_id (Optional[UUID]): The unique identifier for the address, defaults to None.
    """
    address_id: Optional[UUID] = None

    class Config:
        from_attributes = True


class AddressCreateSchema(AddressBase):
    """
    Schema for creating a new address.

    Inherits from AddressBase.
    """
    class Config:
        from_attributes = True


# Ensure pydantic schema is initialized TODO: Remove
AddressCreateSchema.model_rebuild()


class EntityAddressBase(BaseModel):
    """
    Base model for representing an entity's address association.

    Attributes:
        entity_type (str): The type of the entity.
        entity_id (Optional[str|UUID]): The unique identifier for the entity.
        address_id (str|UUID): The unique identifier for the address.
        emergency_address (Optional[bool]): Indicates if this is an emergency address, defaults to False.
        emergency_address_hash (Optional[str]): A hash value for the emergency address, defaults to an empty string.
    """
    entity_type: str
    entity_id: Optional[str | UUID]
    address_id: str | UUID
    emergency_address: Optional[bool] = False
    emergency_address_hash: Optional[str] = ""

    class Config:
        from_attributes = True


class EntityAddress(EntityAddressBase):
    """
    Model for representing an entity's address association with an additional association ID.

    Attributes:
        entity_assoc_id (str|UUID): The unique identifier for the entity-address association.
    """
    entity_assoc_id: str | UUID

    class Config:
        from_attributes = True


class EntityAddressCreate(EntityAddressBase):
    """
    Schema for creating a new entity's address association.

    Inherits from EntityAddressBase.
    """
    class Config:
        from_attributes = True


class EntityAddressUpdate(EntityAddressBase):
    """
    Schema for updating an existing entity's address association.

    Inherits from EntityAddressBase.
    """
    class Config:
        from_attributes = True
