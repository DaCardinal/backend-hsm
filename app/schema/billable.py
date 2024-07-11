from uuid import UUID
from pydantic import BaseModel, constr
from typing import Optional, Annotated

class EntityBillableBase(BaseModel):
    """
    Base model for entity billable information.

    Attributes:
        billable_id (UUID): The unique identifier for the billable entity.
        payment_type_id (UUID): The unique identifier for the payment type.
        billable_amount (str): The amount for the billable entity.
        apply_to_units (bool): Indicates whether the billable entity applies to units.
    """
    billable_id: UUID
    payment_type_id: UUID
    billable_amount: Annotated[str, constr(max_length=100)]
    apply_to_units: bool


class EntityBillable(BaseModel):
    """
    Model for representing an entity billable with additional details.

    Attributes:
        entity_billable_id (UUID): The unique identifier for the entity billable.
        payment_type_id (UUID): The unique identifier for the payment type.
        entity_assoc_id (UUID): The unique identifier for the associated entity.
        entity_type (str): The type of the entity.
        billable_assoc_id (UUID): The unique identifier for the billable association.
        billable_type (str): The type of the billable entity.
        billable_amount (Optional[int]): The amount for the billable entity.
        apply_to_units (Optional[bool]): Indicates whether the billable entity applies to units.
    """
    entity_billable_id: UUID
    payment_type_id: UUID
    entity_assoc_id: UUID
    entity_type: Annotated[str, constr(max_length=50)]
    billable_assoc_id: UUID
    billable_type: Annotated[str, constr(max_length=50)]
    billable_amount: Optional[int] = None
    apply_to_units: Optional[bool] = False

    class Config:
        from_attributes = True


class EntityBillableCreate(BaseModel):
    """
    Schema for creating an entity billable.

    Attributes:
        billable_id (Optional[UUID]): The unique identifier for the billable entity.
        payment_type (Optional[str]): The type of payment for the billable entity.
        billable_amount (Optional[int]): The amount for the billable entity.
        apply_to_units (Optional[bool]): Indicates whether the billable entity applies to units.
    """
    billable_id: Optional[UUID] = None
    payment_type: Optional[Annotated[str, constr(max_length=50)]] = None
    billable_amount: Optional[int] = None
    apply_to_units: Optional[bool] = False


class EntityBillableUpdate(EntityBillableBase):
    """
    Schema for updating an entity billable.

    Inherits from EntityBillableBase.
    """
    pass


class UtilitiesBase(BaseModel):
    """
    Base model for utilities information.

    Attributes:
        name (str): The name of the utility.
        description (Optional[str]): The description of the utility.
    """
    name: Annotated[str, constr(max_length=100)]
    description: Optional[Annotated[str, constr(max_length=255)]] = None

    class Config:
        from_attributes = True


class Utilities(UtilitiesBase):
    """
    Model for representing utilities with additional details.

    Attributes:
        utility_id (UUID): The unique identifier for the utility.
        billable_amount (Optional[str]): The amount for the utility.
        apply_to_units (Optional[bool]): Indicates whether the utility applies to units.
    """
    utility_id: UUID
    billable_amount: Optional[Annotated[str, constr(max_length=100)]] = None
    apply_to_units: Optional[bool] = None

    class Config:
        from_attributes = True


class UtilitiesCreateSchema(UtilitiesBase):
    """
    Schema for creating utilities.

    Inherits from UtilitiesBase.
    """
    pass


class UtilitiesUpdateSchema(UtilitiesBase):
    """
    Schema for updating utilities.

    Inherits from UtilitiesBase.
    """
    pass