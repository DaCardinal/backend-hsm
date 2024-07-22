from uuid import UUID
from typing import Optional
from pydantic import BaseModel, ConfigDict

# mixins
from app.schema.mixins.address_mixin import AddressBase


class AddressCreateSchema(AddressBase):
    """
    Schema for creating a new address.

    Inherits from AddressBase.
    """

    model_config = ConfigDict(from_attributes=True)


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

    model_config = ConfigDict(from_attributes=True)


class EntityAddress(EntityAddressBase):
    """
    Model for representing an entity's address association with an additional association ID.

    Attributes:
        entity_assoc_id (str|UUID): The unique identifier for the entity-address association.
    """

    entity_assoc_id: str | UUID

    model_config = ConfigDict(from_attributes=True)


class EntityAddressCreate(EntityAddressBase):
    """
    Schema for creating a new entity's address association.

    Inherits from EntityAddressBase.
    """

    model_config = ConfigDict(from_attributes=True)


class EntityAddressUpdate(EntityAddressBase):
    """
    Schema for updating an existing entity's address association.

    Inherits from EntityAddressBase.
    """

    model_config = ConfigDict(from_attributes=True)
