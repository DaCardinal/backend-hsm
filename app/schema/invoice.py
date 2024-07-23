from uuid import UUID
from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, ConfigDict, constr
from typing import List, Optional, Union, Annotated

# schemas
from app.schema.user import UserBase
from app.schema.enums import PaymentStatus, InvoiceType
from app.schema.mixins.property_mixin import (
    Property,
    PropertyUnit,
    PropertyDetailsMixin,
)
from app.schema.mixins.invoice_mixin import (
    InvoiceItemBase,
    InvoiceBase,
    InvoiceItemMixin,
)

# models
from app.models.invoice import Invoice as InvoiceModel


class InvoiceItemUpdateSchema(InvoiceItemBase):
    """
    Schema for updating an invoice item.

    Attributes:
        invoice_item_id (Optional[UUID]): The unique identifier for the invoice item.
    """

    invoice_item_id: Optional[UUID] = None

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        use_enum_values=True,
    )


class InvoiceItemCreateSchema(InvoiceItemBase):
    """
    Schema for creating an invoice item.

    Inherits from InvoiceItemBase.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        use_enum_values=True,
    )


class InvoiceCreateSchema(InvoiceBase):
    """
    Schema for creating an invoice.

    Inherits from InvoiceBase.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        use_enum_values=True,
    )


class InvoiceUpdateSchema(InvoiceBase):
    """
    Schema for updating an invoice.

    Attributes:
        id (Optional[UUID]): The unique identifier for the invoice.
        invoice_number (Optional[str]): The number of the invoice.
    """

    id: Optional[UUID] = None
    invoice_number: Optional[Annotated[str, constr(max_length=50)]] = None

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        use_enum_values=True,
    )


class InvoiceResponse(BaseModel, InvoiceItemMixin):
    """
    Model for representing an invoice response.

    Attributes:
        id (Optional[UUID]): The unique identifier for the invoice.
        invoice_number (Optional[str]): The number of the invoice.
        issued_by (Optional[UUID | UserBase]): The issuer of the invoice.
        issued_to (Optional[UUID | UserBase]): The recipient of the invoice.
        invoice_details (Optional[str]): The details of the invoice.
        invoice_amount (Decimal): The total amount of the invoice.
        due_date (Optional[datetime]): The due date of the invoice.
        date_paid (Optional[datetime]): The date the invoice was paid.
        status (PaymentStatusEnum): The status of the payment.
        transaction_id (Optional[UUID]): The transaction ID for the payment.
        invoice_items (List[InvoiceItemBase]): The items in the invoice.
    """

    id: Optional[UUID] = None
    invoice_number: Optional[Annotated[str, constr(max_length=50)]] = None
    issued_by: Optional[Union[UUID, UserBase]] = None
    issued_to: Optional[Union[UUID, UserBase]] = None
    invoice_details: Optional[Annotated[str, constr(max_length=255)]] = None
    invoice_amount: Decimal
    due_date: Optional[datetime] = None
    date_paid: Optional[datetime] = None
    status: PaymentStatus
    transaction_id: Optional[UUID] = None
    invoice_items: List[InvoiceItemBase] = []

    @classmethod
    def from_orm_model(cls, invoice: InvoiceModel) -> "InvoiceResponse":
        """
        Create an InvoiceResponse instance from an ORM model.

        Args:
            invoice (InvoiceModel): Invoice ORM model.

        Returns:
            InvoiceResponse: Invoice response object.
        """
        return cls(
            id=invoice.id,
            invoice_number=invoice.invoice_number,
            issued_by=invoice.issued_by_user,
            issued_to=invoice.issued_to_user,
            invoice_details=invoice.invoice_details,
            invoice_amount=invoice.invoice_amount,
            due_date=invoice.due_date,
            date_paid=invoice.date_paid,
            status=invoice.status,
            transaction_id=invoice.transaction_id,
            invoice_items=cls.get_invoice_items(invoice.invoice_items),
        ).model_dump()


class InvoiceDueResponse(BaseModel, InvoiceItemMixin, PropertyDetailsMixin):
    """
    Model for representing an invoice due response.

    Attributes:
        id (Optional[UUID]): The unique identifier for the invoice.
        invoice_number (Optional[str]): The number of the invoice.
        issued_by (Optional[UUID | UserBase]): The issuer of the invoice.
        issued_to (Optional[UUID | UserBase]): The recipient of the invoice.
        invoice_details (Optional[str]): The details of the invoice.
        invoice_amount (Decimal): The total amount of the invoice.
        due_date (Optional[datetime]): The due date of the invoice.
        date_paid (Optional[datetime]): The date the invoice was paid.
        status (PaymentStatusEnum): The status of the payment.
        transaction_id (Optional[UUID]): The transaction ID for the payment.
        invoice_items (List[InvoiceItemBase]): The items in the invoice.
    """

    id: Optional[UUID] = None
    invoice_number: Optional[Annotated[str, constr(max_length=50)]] = None
    issued_by: Optional[Union[UUID, UserBase]] = None
    issued_to: Optional[Union[UUID, UserBase]] = None
    invoice_details: Optional[Annotated[str, constr(max_length=255)]] = None
    invoice_amount: Decimal
    due_date: Optional[datetime] = None
    date_paid: Optional[datetime] = None
    invoice_type: InvoiceType
    status: PaymentStatus
    transaction_id: Optional[UUID] = None
    invoice_items: List[InvoiceItemBase] = []
    property: Optional[List[Union[Property, PropertyUnit]]]

    @classmethod
    def from_orm_model(cls, invoice: InvoiceModel) -> "InvoiceResponse":
        """
        Create an InvoiceDueResponse instance from an ORM model.

        Args:
            invoice (InvoiceModel): Invoice ORM model.

        Returns:
            InvoiceResponse: Invoice response object.
        """
        return cls(
            id=invoice.id,
            invoice_number=invoice.invoice_number,
            issued_by=invoice.issued_by_user,
            issued_to=invoice.issued_to_user,
            invoice_details=invoice.invoice_details,
            invoice_amount=invoice.invoice_amount,
            due_date=invoice.due_date,
            date_paid=invoice.date_paid,
            invoice_type =invoice.invoice_type,
            status=invoice.status,
            transaction_id=invoice.transaction_id,
            invoice_items=cls.get_invoice_items(invoice.invoice_items),
            property=cls.get_property_details_from_contract(invoice.contracts),
        ).model_dump()
