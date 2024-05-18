from uuid import UUID
from decimal import Decimal
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from app.models import Contract as ContractModel, ContractType as ContractTypeModel, PaymentTypes as PaymentTypeModel


class ContractType(BaseModel):
    contract_type_id: UUID = Field(...)
    contract_type_name: Optional[str] = Field(max_length=128)
    fee_percentage: Optional[Decimal] = Field(max_length=5)

    class Config:
        from_attributes = True

class PaymentType(BaseModel):
    payment_type_id: UUID = Field(...)
    payment_type_name: Optional[str] = Field(max_length=80)
    payment_type_description: Optional[str]
    num_of_invoices: Optional[Decimal] = Field(max_length=10)

    class Config:
        from_attributes = True

class ContractBase(BaseModel):
    contract_type: str = Field(..., max_length=128)
    payment_type: str = Field(..., max_length=128)
    contract_status: str = Field(..., max_length=128)
    contract_details: str = Field(..., max_length=50)
    num_invoices: int = Field(..., max_length=50)
    payment_amount: float = Field(..., max_length=50)
    fee_percentage: float = Field(..., max_length=50)
    fee_amount: float = Field(..., max_length=50)
    date_signed: datetime = Field(default_factory=datetime.now)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    class Config:
        from_attributes = True
        use_enum_values = True

class ContractCreateSchema(ContractBase):
    class Config:
        from_attributes = True

class ContractUpdateSchema(ContractBase):
    class Config:
        from_attributes = True

class Contract(ContractBase):
    contract_id: UUID = Field(...)

    class Config:
        from_attributes = True

class ContractResponse(BaseModel):
    contract_id: UUID = Field(...)
    contract_type: str = Field(..., max_length=128)
    payment_type: str = Field(..., max_length=128)
    contract_status: str = Field(..., max_length=128)
    contract_details: str = Field(..., max_length=50)
    num_invoices: int = Field(..., max_length=50)
    payment_amount: float = Field(..., max_length=50)
    fee_percentage: float = Field(..., max_length=50)
    fee_amount: float = Field(..., max_length=50)
    date_signed: datetime = Field(default_factory=datetime.now)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    @classmethod
    def get_contract_type(cls, contract_type: ContractTypeModel):
        result : ContractType = contract_type
    
        return result.contract_type_name
    
    @classmethod
    def get_payment_type(cls, payment_type: PaymentTypeModel):
        result : PaymentType = payment_type
    
        return result.payment_type_name
    
    @classmethod
    def from_orm_model(cls, contract: ContractModel):

        result = cls(
            # contract_id = contract.contract_id,
            contract_type = cls.get_contract_type(contract.contract_type_id),
            payment_type = cls.get_payment_type(contract.payment_type_id),
            contract_status = contract.contract_status,
            contract_details = contract.contract_details,
            num_invoices = contract.num_invoices,
            payment_amount = contract.payment_amount,
            fee_percentage = contract.fee_percentage,
            fee_amount = contract.fee_amount,
            date_signed = contract.date_signed,
            start_date = contract.start_date,
            end_date = contract.end_date,
        ).model_dump()
        
        return result