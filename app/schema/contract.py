from enum import Enum
from uuid import UUID
from decimal import Decimal
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from app.models import Contract as ContractModel, UnderContract
from app.schema import UserBase, PropertyUnitAssoc, Property

class ContractStatus(str, Enum):
    active = "active"
    expired = "expired"
    terminated = "terminated"

class UnderContractSchema(BaseModel):
    id: Optional[UUID] = None
    property_unit_assoc: Optional[UUID | Property] = Field(None, alias='property')
    contract_id: Optional[UUID] = None
    contract_status: ContractStatus = None
    client_id: Optional[UUID | UserBase] = None
    employee_id: Optional[UUID | UserBase] = None

    class Config:
        from_attributes = True
        use_enum_values = True
        populate_by_name = True

class ContractType(BaseModel):
    contract_type_id: UUID = Field(...)
    contract_type_name: Optional[str] = Field(max_length=128)
    fee_percentage: Optional[Decimal]

    class Config:
        from_attributes = True

class PaymentType(BaseModel):
    payment_type_id: UUID = Field(...)
    payment_type_name: Optional[str] = Field(max_length=80)
    payment_type_description: Optional[str]
    num_of_invoices: Optional[Decimal]

    class Config:
        from_attributes = True
        arbitrary_types_allowed=True

class ContractBase(BaseModel):
    contract_type: str
    payment_type: str
    contract_status: ContractStatus = Field(...)
    contract_details: str
    num_invoices: int
    payment_amount: int
    fee_percentage: int
    fee_amount: int
    date_signed: datetime = Field(default_factory=datetime.now)
    start_date: Optional[datetime] = Field(default_factory=datetime.now)
    end_date: Optional[datetime] = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True
        use_enum_values = True

class ContractCreateSchema(BaseModel):
    contract_type: str
    payment_type: str
    contract_status: ContractStatus = Field(...)
    contract_details: str
    payment_amount: Decimal
    fee_percentage: Decimal
    fee_amount: Decimal
    date_signed: datetime = Field(default_factory=datetime.now)
    start_date: Optional[datetime] = Field(default_factory=datetime.now)
    end_date: Optional[datetime] = Field(default_factory=datetime.now)
    contract_info: Optional[List[UnderContractSchema] | UnderContractSchema] = None

    class Config:
        from_attributes = True
        use_enum_values = True

class ContractUpdateSchema(BaseModel):
    contract_type: str
    payment_type: str
    contract_status: ContractStatus = Field(...)
    contract_details: str
    payment_amount: Decimal
    fee_percentage: Decimal
    fee_amount: Decimal
    date_signed: datetime = Field(default_factory=datetime.now)
    start_date: Optional[datetime] = Field(default_factory=datetime.now)
    end_date: Optional[datetime] = Field(default_factory=datetime.now)
    contract_info: Optional[List[UnderContractSchema] | UnderContractSchema] = None

    class Config:
        from_attributes = True

class Contract(ContractBase):
    contract_id: UUID = Field(...)

    class Config:
        from_attributes = True

class ContractResponse(BaseModel):
    contract_id: Optional[UUID]
    contract_type: Optional[str] = Field(..., max_length=128)
    payment_type: Optional[str] = Field(..., max_length=128)
    contract_status: str = Field(..., max_length=128)
    contract_details: str = Field(..., max_length=50)
    num_invoices: Optional[int]
    payment_amount: float
    fee_percentage: float
    fee_amount: float
    date_signed: datetime = Field(default_factory=datetime.now)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    contract_info: Optional[List[UnderContractSchema]] = None
    
    @classmethod
    def get_property_info(cls, property_unit_assoc: PropertyUnitAssoc):
        property : Property = property_unit_assoc.property

        return Property(
            property_unit_assoc_id = property.property_unit_assoc_id,
            property_id = property.property_id,
            name = property.name,
            property_type = property.property_type.name,
            amount = property.amount,
            security_deposit = property.security_deposit,
            commission = property.commission,
            floor_space = property.floor_space,
            num_units = property.num_units,
            num_bathrooms = property.num_bathrooms,
            num_garages = property.num_garages,
            has_balconies = property.has_balconies,
            has_parking_space = property.has_parking_space,
            pets_allowed = property.pets_allowed,
            description = property.description,
            property_status = property.property_status,
        )
    
    @classmethod
    def get_user_info(cls, user: UserBase):

        return UserBase(
            user_id=user.user_id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            gender=user.gender,
            phone_number=user.phone_number,
            photo_url=user.photo_url,
            identification_number=user.identification_number,
            date_of_birth=user.date_of_birth
        )
    
    @classmethod
    def get_contract_details(cls, contract_details: List[UnderContract]):
        result = []

        for contract_detail in contract_details:
            result.append(UnderContractSchema(
                id = contract_detail.id,
                property_unit_assoc = cls.get_property_info(contract_detail.properties),
                contract_id = contract_detail.contract_id,
                contract_status = contract_detail.contract_status,
                client_id = cls.get_user_info(contract_detail.client_representative),
                employee_id = cls.get_user_info(contract_detail.employee_representative),
            ))

        return result
        
    @classmethod
    def from_orm_model(cls, contract: ContractModel):
        result = cls(
            contract_id = contract.contract_id,
            contract_type = contract.contract_type_value,
            payment_type = contract.payment_type_value,
            contract_status = contract.contract_status,
            contract_details = contract.contract_details,
            num_invoices = contract.num_invoices,
            payment_amount = contract.payment_amount,
            fee_percentage = contract.fee_percentage,
            fee_amount = contract.fee_amount,
            date_signed = contract.date_signed,
            start_date = contract.start_date,
            end_date = contract.end_date,
            contract_info = cls.get_contract_details(contract.under_contract)
        ).model_dump()

        return result