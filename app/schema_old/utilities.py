from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel

class EntityBillableBase(BaseModel):
    billable_id: UUID
    payment_type_id: UUID
    billable_amount: str
    apply_to_units: bool

class EntityBillableCreate(BaseModel):
    billable_id: Optional[UUID] = None
    payment_type: Optional[str]
    billable_amount: Optional[int]
    apply_to_units: Optional[bool] = False

class EntityBillableUpdate(EntityBillableBase):
    pass

class EntityBillable(BaseModel):
    entity_billable_id: UUID
    # billable_id: UUID
    payment_type_id: UUID
    entity_assoc_id: UUID
    entity_type: str
    billable_assoc_id: UUID
    billable_type: str
    billable_amount: Optional[int]
    apply_to_units: Optional[bool] = False

    class Config:
        from_attributes = True

class UtilitiesBase(BaseModel):
    name: str
    description: Optional[str]

    class Config:
        from_attributes = True

class UtilitiesCreateSchema(UtilitiesBase):
    pass

class UtilitiesUpdateSchema(UtilitiesBase):
    pass

class Utilities(UtilitiesBase):
    utility_id: UUID
    billable_amount: Optional[str] = None
    apply_to_units: Optional[bool] = None

    class Config:
        from_attributes = True