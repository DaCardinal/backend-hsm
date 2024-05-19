from enum import Enum
from uuid import UUID
from decimal import Decimal
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from app.models import Invoice as InvoiceModel, InvoiceItem

class PaymentStatusEnum(str, Enum):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"

class InvoiceItemBase(BaseModel):
    description: str = Field(alias='description')
    quantity: int = Field(alias='quantity')
    unit_price: Decimal = Field(alias='unit_price')
    total_price: Decimal = Field(alias='total_price')

    class Config:
        from_attributes = True
        use_enum_values = True
        populate_by_name = True

class InvoiceItemUpdate(InvoiceItemBase):
    invoice_item_id: Optional[UUID] = Field(None, alias='invoice_item_id')

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
    issued_by: Optional[str] = Field(None, alias='issued_by')
    issued_to: Optional[str] = Field(None, alias='issued_to')
    invoice_details: Optional[str] = Field(None, alias='invoice_details')
    invoice_amount: Decimal = Field(alias='invoice_amount')
    due_date: Optional[datetime] = Field(None, alias='due_date')
    date_paid: Optional[datetime] = Field(None, alias='date_paid')
    status: PaymentStatusEnum = Field(alias='status')
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
    issued_by: Optional[str] = Field(None, alias='issued_by')
    issued_to: Optional[str] = Field(None, alias='issued_to')
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
                description=invoice.description,
                quantity = invoice.quantity,
                unit_price= invoice.unit_price,
                total_price= invoice.total_price
            ))

        return result
    
    @classmethod
    def from_orm_model(cls, invoice: InvoiceModel):
        result = cls(
            id = invoice.id,
            invoice_number = invoice.invoice_number,
            issued_by = invoice.issued_by,
            issued_to = invoice.issued_to,
            invoice_details = invoice.invoice_details,
            invoice_amount = invoice.invoice_amount,
            due_date = invoice.due_date,
            date_paid = invoice.date_paid,
            status = invoice.status,
            transaction_id = invoice.transaction_id,
            invoice_items = cls.get_invoice_items(invoice.invoice_items)
        ).model_dump()

        return result
    