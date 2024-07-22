from uuid import UUID
from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, ConfigDict, constr
from typing import List, Optional, Annotated

# schemas
from app.schema.enums import ContractStatus
from app.schema.billable import EntityBillableCreate

# mixins
from app.schema.mixins.billable_mixin import UtilityInfo
from app.schema.mixins.contract_mixin import ContractInfoMixin
from app.schema.mixins.contract_mixin import UnderContractSchema

# models
from app.models.contract import Contract as ContractModel


class ContractType(BaseModel):
    """
    Schema for representing a contract type.

    Attributes:
        contract_type_id (UUID): The unique identifier for the contract type.
        contract_type_name (Optional[str]): The name of the contract type (max length 128).
        fee_percentage (Optional[Decimal]): The fee percentage for the contract type.
    """

    contract_type_id: UUID
    contract_type_name: Optional[Annotated[str, constr(max_length=128)]] = None
    fee_percentage: Optional[Decimal] = None

    model_config = ConfigDict(from_attributes=True)


class ContractBase(BaseModel):
    """
    Base schema for representing contract information.

    Attributes:
        contract_type (str): The type of the contract.
        payment_type (str): The type of payment for the contract.
        contract_status (ContractStatus): The status of the contract.
        contract_details (str): The details of the contract.
        num_invoices (int): The number of invoices for the contract.
        payment_amount (int): The payment amount for the contract.
        fee_percentage (int): The fee percentage for the contract.
        fee_amount (int): The fee amount for the contract.
        date_signed (datetime): The date the contract was signed.
        start_date (Optional[datetime]): The start date of the contract.
        end_date (Optional[datetime]): The end date of the contract.
    """

    contract_type: str
    payment_type: str
    contract_status: ContractStatus
    contract_details: str
    num_invoices: int
    payment_amount: int
    fee_percentage: int
    fee_amount: int
    date_signed: datetime = datetime.now()
    start_date: Optional[datetime] = datetime.now()
    end_date: Optional[datetime] = datetime.now()

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class Contract(ContractBase):
    """
    Model for representing a contract with additional details.

    Attributes:
        contract_id (UUID): The unique identifier for the contract.
    """

    contract_id: UUID

    model_config = ConfigDict(from_attributes=True)


class ContractCreateSchema(BaseModel):
    """
    Schema for creating a new contract.

    Attributes:
        contract_type (str): The type of the contract.
        payment_type (str): The type of payment for the contract.
        contract_status (ContractStatus): The status of the contract.
        contract_details (Optional[str]): The details of the contract.
        payment_amount (Decimal): The payment amount for the contract.
        fee_percentage (Optional[Decimal]): The fee percentage for the contract.
        fee_amount (Optional[Decimal]): The fee amount for the contract.
        date_signed (datetime): The date the contract was signed.
        start_date (Optional[datetime]): The start date of the contract.
        end_date (Optional[datetime]): The end date of the contract.
        contract_info (Optional[List[UnderContractSchema] | UnderContractSchema]): The information of the under-contract relationships.
        utilities (Optional[List[EntityBillableCreate] | EntityBillableCreate]): The utilities associated with the contract.
    """

    contract_type: str
    payment_type: str
    contract_status: ContractStatus
    contract_details: Optional[str] = None
    payment_amount: Decimal
    fee_percentage: Optional[Decimal] = None
    fee_amount: Optional[Decimal] = None
    date_signed: datetime = datetime.now()
    start_date: Optional[datetime] = datetime.now()
    end_date: Optional[datetime] = None
    contract_info: Optional[List[UnderContractSchema] | UnderContractSchema] = None
    utilities: Optional[List[EntityBillableCreate] | EntityBillableCreate] = None

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class ContractUpdateSchema(BaseModel):
    """
    Schema for updating an existing contract.

    Attributes:
        contract_type (Optional[str]): The type of the contract.
        payment_type (Optional[str]): The type of payment for the contract.
        contract_status (Optional[ContractStatus]): The status of the contract.
        contract_details (Optional[str]): The details of the contract.
        payment_amount (Optional[Decimal]): The payment amount for the contract.
        fee_percentage (Optional[Decimal]): The fee percentage for the contract.
        fee_amount (Optional[Decimal]): The fee amount for the contract.
        date_signed (Optional[datetime]): The date the contract was signed.
        start_date (Optional[datetime]): The start date of the contract.
        end_date (Optional[datetime]): The end date of the contract.
        contract_info (Optional[List[UnderContractSchema] | UnderContractSchema]): The information of the under-contract relationships.
        utilities (Optional[List[EntityBillableCreate] | EntityBillableCreate]): The utilities associated with the contract.
    """

    contract_type: Optional[str] = None
    payment_type: Optional[str] = None
    contract_status: Optional[ContractStatus] = None
    contract_details: Optional[str] = None
    payment_amount: Optional[Decimal] = None
    fee_percentage: Optional[Decimal] = None
    fee_amount: Optional[Decimal] = None
    date_signed: Optional[datetime] = datetime.now()
    start_date: Optional[datetime] = datetime.now()
    end_date: Optional[datetime] = None
    contract_info: Optional[List[UnderContractSchema] | UnderContractSchema] = None
    utilities: Optional[List[EntityBillableCreate] | EntityBillableCreate] = None

    model_config = ConfigDict(from_attributes=True)


class ContractResponse(BaseModel, ContractInfoMixin):
    """
    Schema for representing a contract response.

    Attributes:
        contract_id (Optional[UUID]): The unique identifier for the contract.
        contract_number (Optional[str]): The number of the contract (max length 128).
        contract_type (Optional[str]): The type of the contract (max length 128).
        payment_type (Optional[str]): The type of payment for the contract (max length 128).
        contract_status (str): The status of the contract (max length 128).
        contract_details (Optional[str]): The details of the contract (max length 128).
        num_invoices (Optional[int]): The number of invoices for the contract.
        payment_amount (float): The payment amount for the contract.
        fee_percentage (float): The fee percentage for the contract.
        fee_amount (float): The fee amount for the contract.
        date_signed (datetime): The date the contract was signed.
        start_date (Optional[datetime]): The start date of the contract.
        end_date (Optional[datetime]): The end date of the contract.
        contract_info (Optional[List[UnderContractSchema]]): The information of the under-contract relationships.
        utilities (Optional[List[Any]]): The utilities associated with the contract.
    """

    contract_id: Optional[UUID] = None
    contract_number: Optional[Annotated[str, constr(max_length=128)]] = None
    contract_type: Optional[Annotated[str, constr(max_length=128)]] = None
    payment_type: Optional[Annotated[str, constr(max_length=128)]] = None
    contract_status: Annotated[str, constr(max_length=128)]
    contract_details: Optional[Annotated[str, constr(max_length=128)]] = None
    num_invoices: Optional[int] = None
    payment_amount: float
    fee_percentage: float
    fee_amount: float
    date_signed: datetime = datetime.now()
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    contract_info: Optional[List[UnderContractSchema]] = None
    utilities: Optional[List[UtilityInfo]] = None

    @classmethod
    def from_orm_model(cls, contract: ContractModel):
        """
        Create a ContractResponse instance from an ORM model.

        Args:
            contract (ContractModel): Contract ORM model.

        Returns:
            ContractResponse: Contract response object.
        """
        return cls(
            contract_id=contract.contract_id,
            contract_number=contract.contract_number,
            contract_type=contract.contract_type_value,
            payment_type=contract.payment_type_value,
            contract_status=contract.contract_status,
            contract_details=contract.contract_details,
            num_invoices=contract.num_invoices,
            payment_amount=contract.payment_amount,
            fee_percentage=contract.fee_percentage,
            fee_amount=contract.fee_amount,
            date_signed=contract.date_signed,
            start_date=contract.start_date,
            end_date=contract.end_date,
            contract_info=cls.get_contract_details(contract.under_contract),
            utilities=cls.get_utilities_info(contract.utilities),
        ).model_dump()
