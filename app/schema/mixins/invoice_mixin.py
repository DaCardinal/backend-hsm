from uuid import UUID
from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, ConfigDict, constr
from typing import List, Optional, Union, Annotated

from app.schema.enums import InvoiceType, PaymentStatus
from app.schema.mixins.user_mixins import UserBase


class InvoiceItemBase(BaseModel):
    """
    Base model for invoice item information.

    Attributes:
        quantity (int): The quantity of the invoice item.
        unit_price (Decimal): The unit price of the invoice item.
        total_price (Decimal): The total price of the invoice item.
        reference_id (Optional[str]): The reference ID for the invoice item.
        description (Optional[str]): The description of the invoice item.
    """

    quantity: int
    unit_price: Decimal
    total_price: Decimal
    reference_id: Optional[Annotated[str, constr(max_length=255)]] = None
    description: Optional[Annotated[str, constr(max_length=255)]] = None

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        use_enum_values=True,
    )


class InvoiceItem(BaseModel):
    """
    Model for representing an invoice item with additional details.

    Attributes:
        quantity (int): The quantity of the invoice item.
        unit_price (Decimal): The unit price of the invoice item.
        total_price (Decimal): The total price of the invoice item.
        invoice_item_id (UUID): The unique identifier for the invoice item.
        invoice_number (UUID): The unique identifier for the invoice.
        reference_id (Optional[str]): The reference ID for the invoice item.
        description (Optional[str]): The description of the invoice item.
    """

    quantity: int
    unit_price: Decimal
    total_price: Decimal
    invoice_item_id: UUID
    invoice_number: UUID
    reference_id: Optional[Annotated[str, constr(max_length=255)]] = None
    description: Optional[Annotated[str, constr(max_length=255)]] = None

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        use_enum_values=True,
    )


class InvoiceBase(BaseModel):
    """
    Base model for invoice information.

    Attributes:
        issued_by (Optional[UUID | UserBase]): The issuer of the invoice.
        issued_to (Optional[UUID | UserBase]): The recipient of the invoice.
        invoice_details (Optional[str]): The details of the invoice.
        due_date (Optional[datetime]): The due date of the invoice.
        date_paid (Optional[datetime]): The date the invoice was paid.
        status (PaymentStatusEnum | str): The status of the payment.
        transaction_id (Optional[UUID]): The transaction ID for the payment.
        invoice_items (List[InvoiceItemBase]): The items in the invoice.
    """

    issued_by: Optional[Union[UUID, UserBase]] = None
    issued_to: Optional[Union[UUID, UserBase]] = None
    invoice_details: Optional[Annotated[str, constr(max_length=255)]] = None
    due_date: Optional[datetime] = None
    date_paid: Optional[datetime] = None
    status: Union[PaymentStatus, Annotated[str, constr(max_length=50)]]
    invoice_type: Union[InvoiceType, Annotated[str, constr(max_length=50)]]
    transaction_id: Optional[UUID] = None
    invoice_items: List[InvoiceItemBase] = []

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        use_enum_values=True,
    )


class Invoice(BaseModel):
    """
    Base model for invoice information.

    Attributes:
        invoice_number (Optional[str]): The number of the invoice.
        issued_by (Optional[UUID | UserBase]): The issuer of the invoice.
        issued_to (Optional[UUID | UserBase]): The recipient of the invoice.
        invoice_details (Optional[str]): The details of the invoice.
        due_date (Optional[datetime]): The due date of the invoice.
        date_paid (Optional[datetime]): The date the invoice was paid.
        status (PaymentStatusEnum | str): The status of the payment.
        transaction_id (Optional[UUID]): The transaction ID for the payment.
        invoice_items (List[InvoiceItemBase]): The items in the invoice.
    """

    invoice_number: Optional[str]
    issued_by: Optional[Union[UUID, UserBase]] = None
    issued_to: Optional[Union[UUID, UserBase]] = None
    invoice_details: Optional[Annotated[str, constr(max_length=255)]] = None
    due_date: Optional[datetime] = None
    date_paid: Optional[datetime] = None
    status: Union[PaymentStatus, Annotated[str, constr(max_length=50)]]
    transaction_id: Optional[UUID] = None
    invoice_items: List[InvoiceItemBase] = []

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        use_enum_values=True,
    )


class InvoiceItemMixin:
    @classmethod
    def get_invoice_items(
        cls, invoice_details: List[InvoiceItem]
    ) -> List[InvoiceItemBase]:
        """
        Get the items in the invoice.

        Args:
            invoice_details (List[InvoiceItem]): List of invoice items.

        Returns:
            List[InvoiceItemBase]: List of invoice item base objects.
        """
        result = []
        for invoice in invoice_details:
            result.append(
                InvoiceItemBase(
                    reference_id=invoice.reference_id,
                    description=invoice.description,
                    quantity=invoice.quantity,
                    unit_price=invoice.unit_price,
                    total_price=invoice.total_price,
                )
            )
        return result
