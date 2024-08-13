from uuid import UUID
from typing import Any, Optional, Annotated, Union
from pydantic import BaseModel, ConfigDict, constr

from app.models.entity_billable import EntityBillable as EntityBillableModel
from app.schema.enums import PaymentStatus


class BillableBase(BaseModel):
    """
    Base model for entity billable information.

    Attributes:
        payment_type_id (UUID): The unique identifier for the payment type.
        billable_amount (str): The amount for the billable entity.
        apply_to_units (bool): Indicates whether the billable entity applies to units.
    """

    # billable_id: Optional[UUID] = None
    payment_type: Optional[Annotated[str, constr(max_length=50)]] = None
    billable_amount: Optional[int] = None
    apply_to_units: Optional[bool] = False


class Billable(BaseModel):
    """
    Base model for billable information.

    Attributes:
        billable_id (UUID): The unique identifier for the billable entity.
        payment_type_id (UUID): The unique identifier for the payment type.
        billable_amount (str): The amount for the billable entity.
        apply_to_units (bool): Indicates whether the billable entity applies to units.
    """

    billable_id: UUID
    payment_type: Optional[Annotated[str, constr(max_length=50)]] = None
    billable_amount: Optional[int] = None
    apply_to_units: Optional[bool] = False


class EntityBillableBase(BaseModel):
    payment_type_id: UUID
    entity_assoc_id: UUID
    entity_type: Annotated[str, constr(max_length=50)]
    billable_assoc_id: UUID
    billable_type: Annotated[str, constr(max_length=50)]
    billable_amount: Optional[int | str] = None
    apply_to_units: Optional[bool] = False

    model_config = ConfigDict(from_attributes=True)


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

    entity_billable_id: UUID = None
    payment_type_id: Union[UUID | str | Any]
    entity_assoc_id: UUID
    entity_type: Annotated[str, constr(max_length=50)]
    billable_assoc_id: UUID
    billable_type: Annotated[str, constr(max_length=50)]
    billable_amount: Optional[int | str] = None
    apply_to_units: Optional[bool] = False

    model_config = ConfigDict(from_attributes=True)


class EntityBillableResponse(BaseModel):
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

    entity_billable_id: UUID = None
    payment_type_id: Union[UUID | PaymentStatus]
    entity_assoc_id: UUID
    entity_type: Annotated[str, constr(max_length=50)]
    billable_assoc_id: UUID
    billable_type: Annotated[str, constr(max_length=50)]
    billable_amount: Optional[int | str] = None
    apply_to_units: Optional[bool] = False

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm_model(cls, entity_billable: EntityBillableModel):
        return cls(
            entity_billable_id=entity_billable.entity_billable_id,
            payment_type_id=entity_billable.payment_type_id,
            entity_assoc_id=entity_billable.entity_assoc_id,
            entity_type=entity_billable.entity_type,
            billable_assoc_id=entity_billable.billable_assoc_id,
            billable_type=entity_billable.billable_type,
            billable_amount=entity_billable.billable_amount,
            apply_to_units=entity_billable.apply_to_units,
        )


class UtilitiesBase(BaseModel):
    """
    Base model for utilities information.

    Attributes:
        name (str): The name of the utility.
        description (Optional[str]): The description of the utility.
    """

    name: Annotated[str, constr(max_length=100)]
    description: Optional[Annotated[str, constr(max_length=255)]] = None

    model_config = ConfigDict(from_attributes=True)


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

    model_config = ConfigDict(from_attributes=True)


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
