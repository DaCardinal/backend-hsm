from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Union

# schemas
from app.schema.enums import ContractStatus
from app.schema.user import UserBase, User, UserContract as Contract
from app.schema.property import Property, PropertyUnit, PropertyUnitAssoc

class UnderContractBase(BaseModel):
    """
    Base model for under contract information.

    Attributes:
        property_unit_assoc_id (Optional[UUID]): The unique identifier for the associated property unit.
        contract_id (Optional[UUID]): The unique identifier for the contract.
        contract_status (Optional[ContractStatus]): The status of the contract.
        client_id (Optional[UUID]): The unique identifier for the client.
        employee_id (Optional[UUID]): The unique identifier for the employee.
        start_date (Optional[datetime]): The start date of the contract.
        end_date (Optional[datetime]): The end date of the contract.
        properties (Optional[PropertyUnitAssoc]): The associated property unit.
        contract (Optional[Contract]): The associated contract.
        client_representative (Optional[User]): The client representative.
        employee_representative (Optional[User]): The employee representative.
    """
    property_unit_assoc_id: Optional[UUID] = None
    contract_id: Optional[UUID] = None
    contract_status: Optional[ContractStatus] = None
    client_id: Optional[UUID] = None
    employee_id: Optional[UUID] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    properties: Optional[PropertyUnitAssoc] = None
    contract: Optional[Contract] = None
    client_representative: Optional[User] = None
    employee_representative: Optional[User] = None

    class Config:
        from_attributes = True


class UnderContract(UnderContractBase):
    """
    Model for representing an under contract with additional details.

    Attributes:
        under_contract_id (UUID): The unique identifier for the under contract.
    """
    under_contract_id: UUID

    class Config:
        from_attributes = True


class UnderContractCreate(BaseModel):
    """
    Schema for creating an under contract.

    Attributes:
        contract_id (Optional[UUID | str]): The unique identifier for the contract.
        client_id (Optional[UUID]): The unique identifier for the client.
        employee_id (Optional[UUID]): The unique identifier for the employee.
        contract_status (Optional[ContractStatus]): The status of the contract.
        property_unit_assoc (Optional[UUID]): The unique identifier for the associated property unit.
    """
    contract_id: Optional[Union[UUID, str]] = None
    client_id: Optional[UUID] = None
    employee_id: Optional[UUID] = None
    contract_status: Optional[ContractStatus] = None
    property_unit_assoc: Optional[UUID] = None

    class Config:
        from_attributes = True
        use_enum_values = True  # Uses the values of enums instead of their names
        populate_by_name = True  # Allows population by name


class UnderContractUpdate(UnderContractBase):
    """
    Schema for updating an under contract.

    Inherits from UnderContractBase.
    """
    pass


class UnderContractSchema(BaseModel):
    """
    Schema for representing an under-contract relationship.

    Attributes:
        under_contract_id (Optional[UUID]): The unique identifier for the under-contract relationship.
        property_unit_assoc (Optional[UUID | Property | PropertyUnit]): The associated property or property unit.
        contract_id (Optional[UUID]): The unique identifier for the contract.
        contract_status (Optional[ContractStatus]): The status of the contract.
        client_id (Optional[UUID | UserBase]): The unique identifier for the client.
        employee_id (Optional[UUID | UserBase]): The unique identifier for the employee.
    """
    under_contract_id: Optional[UUID] = None
    property_unit_assoc: Optional[UUID | Property | PropertyUnit] = None
    contract_id: Optional[UUID] = None
    contract_status: Optional[ContractStatus] = None
    client_id: Optional[UUID | UserBase] = None
    employee_id: Optional[UUID | UserBase] = None

    class Config:
        from_attributes = True
        use_enum_values = True
        populate_by_name = True