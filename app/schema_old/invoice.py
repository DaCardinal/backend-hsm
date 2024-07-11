from enum import Enum
from uuid import UUID
from decimal import Decimal
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from app.models import Invoice as InvoiceModel, InvoiceItem
from app.schema import UserBase

class PaymentStatusEnum(str, Enum):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"

class InvoiceItemBase(BaseModel):
    # invoice_item_id: Optional[UUID]
    # invoice_number: Optional[UUID]
    reference_id: Optional[str] = None
    description: Optional[str] = None
    quantity: int
    unit_price: Decimal
    total_price: Decimal

    class Config:
        from_attributes = True
        use_enum_values = True
        populate_by_name = True

class InvoiceItem(BaseModel):
    invoice_item_id: UUID
    invoice_number: UUID
    reference_id: Optional[str]
    description: Optional[str]
    quantity: int
    unit_price: Decimal
    total_price: Decimal

    class Config:
        from_attributes = True
        use_enum_values = True
        populate_by_name = True

class InvoiceItemUpdate(InvoiceItemBase):
    invoice_item_id: Optional[UUID] = None

    class Config:
        from_attributes = True
        use_enum_values = True
        populate_by_name = True

class InvoiceItemCreateSchema(InvoiceItemBase):

    class Config:
        from_attributes = True
        use_enum_values = True
        populate_by_name = True

class InvoiceBase(BaseModel):
    issued_by: Optional[UUID | UserBase]
    issued_to:Optional[UUID | UserBase]
    invoice_details: Optional[str] = Field(None, alias='invoice_details')
    due_date: Optional[datetime] = Field(None, alias='due_date')
    date_paid: Optional[datetime] = Field(None, alias='date_paid')
    status: PaymentStatusEnum | str = Field(alias='status')
    transaction_id: Optional[UUID] = Field(None, alias='transaction_id')
    invoice_items: List[InvoiceItemBase] = []

    class Config:
        from_attributes = True
        use_enum_values = True
        populate_by_name = True

class InvoiceCreateSchema(InvoiceBase):

    class Config:
        from_attributes = True
        use_enum_values = True
        populate_by_name = True

class InvoiceUpdateSchema(InvoiceBase):
    id: Optional[UUID] = Field(None, alias='id')
    invoice_number: Optional[str] = Field("", alias='invoice_number')

    class Config:
        from_attributes = True
        use_enum_values = True
        populate_by_name = True

class InvoiceResponse(BaseModel):
    id: Optional[UUID] = Field(None, alias='id')
    invoice_number: Optional[str] = Field("", alias='invoice_number')
    issued_by: Optional[UUID | UserBase]
    issued_to:Optional[UUID | UserBase]
    invoice_details: Optional[str] = Field(None, alias='invoice_details')
    invoice_amount: Decimal = Field(alias='invoice_amount')
    due_date: Optional[datetime] = Field(None, alias='due_date')
    date_paid: Optional[datetime] = Field(None, alias='date_paid')
    status: PaymentStatusEnum = Field(alias='status')
    transaction_id: Optional[UUID] = Field(None, alias='transaction_id')
    invoice_items: List[InvoiceItemBase] = []


    @classmethod
    def get_invoice_items(cls, invoice_details: List[InvoiceItem]):
        result = []

        for invoice in invoice_details:
            result.append(InvoiceItemBase(
                # invoice_item_id=invoice.invoice_item_id,
                description=invoice.description,
                quantity = invoice.quantity,
                unit_price= invoice.unit_price,
                total_price= invoice.total_price,
                reference_id=invoice.reference_id
            ))

        return result
    
    @classmethod
    def from_orm_model(cls, invoice: InvoiceModel):
        result = cls(
            id = invoice.id,
            invoice_number = invoice.invoice_number,
            issued_by = invoice.issued_by_user,
            issued_to = invoice.issued_to_user,
            invoice_details = invoice.invoice_details,
            invoice_amount = invoice.invoice_amount,
            due_date = invoice.due_date,
            date_paid = invoice.date_paid,
            status = invoice.status,
            transaction_id = invoice.transaction_id,
            invoice_items = cls.get_invoice_items(invoice.invoice_items)
        ).model_dump()

        return result
    