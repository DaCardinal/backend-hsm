from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional
from enum import Enum

class ContractStatusEnum(str, Enum):
    active = "active"
    expired = "expired"
    terminated = "terminated"
    pending = "pending"

# Additional Pydantic models for related entities
class PropertyUnitAssoc(BaseModel):
    property_unit_assoc_id: UUID

    class Config:
        from_attributes = True

class Contract(BaseModel):
    contract_id: UUID

    class Config:
        from_attributes = True

class User(BaseModel):
    user_id: UUID

    class Config:
        from_attributes = True

class UnderContractBase(BaseModel):
    property_unit_assoc_id: Optional[UUID]
    contract_id: Optional[UUID]
    contract_status: Optional[ContractStatusEnum]
    client_id: Optional[UUID]
    employee_id: Optional[UUID]
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    properties: Optional[PropertyUnitAssoc] = None
    contract: Optional[Contract] = None
    client_representative: Optional[User] = None
    employee_representative: Optional[User] = None

    class Config:
        from_attributes = True

class UnderContractCreate(BaseModel):
    contract_id: Optional[UUID | str] = None
    client_id: Optional[UUID] = None
    employee_id: Optional[UUID] = None
    contract_status: Optional[ContractStatusEnum] = None
    property_unit_assoc: Optional[UUID]

    class Config:
        from_attributes = True
        use_enum_values = True
        populate_by_name = True

class UnderContractUpdate(UnderContractBase):
    pass

class UnderContractInDBBase(UnderContractBase):
    under_contract_id: UUID

    class Config:
        from_attributes = True

class UnderContract(UnderContractInDBBase):
    pass
    # properties: Optional["PropertyUnitAssoc"] = None
    # contract: Optional["Contract"] = None
    # client_representative: Optional["User"] = None
    # employee_representative: Optional["User"] = None

class UnderContractInDB(UnderContractInDBBase):
    pass