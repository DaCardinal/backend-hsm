from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional, Union

# schemas
from app.schema.enums import ContractStatus
from app.schema.user import User, UserContract as Contract
from app.schema.mixins.property_mixin import PropertyUnitAssoc


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

    model_config = ConfigDict(from_attributes=True)


class UnderContract(UnderContractBase):
    """
    Model for representing an under contract with additional details.

    Attributes:
        under_contract_id (UUID): The unique identifier for the under contract.
    """

    under_contract_id: UUID

    model_config = ConfigDict(from_attributes=True)


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

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        use_enum_values=True,
    )


class UnderContractUpdate(UnderContractBase):
    """
    Schema for updating an under contract.

    Inherits from UnderContractBase.
    """

    pass
