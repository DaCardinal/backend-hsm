from uuid import UUID
from decimal import Decimal
from typing import Optional, Annotated
from pydantic import BaseModel, ConfigDict, constr


class PaymentType(BaseModel):
    """
    Schema for representing a payment type.

    Attributes:
        payment_type_id (UUID): The unique identifier for the payment type.
        payment_type_name (Optional[str]): The name of the payment type (max length 80).
        payment_type_description (Optional[str]): The description of the payment type.
        num_of_invoices (Optional[Decimal]): The number of invoices for the payment type.
    """

    payment_type_id: UUID
    payment_type_name: Optional[Annotated[str, constr(max_length=80)]] = None
    payment_type_description: Optional[str] = None
    num_of_invoices: Optional[Decimal] = None

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
    )
