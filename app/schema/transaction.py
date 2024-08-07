from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict, constr
from typing import Optional, Union, Annotated

# schemas
from app.schema.user import UserBase
from app.schema.enums import PaymentStatus
from app.schema.mixins.user_mixins import UserBaseMixin

# models
from app.models.transaction import Transaction as TransactionModel


class TransactionBase(BaseModel):
    """
    Base model for transaction information.

    Attributes:
        transaction_type (str): The type ID of the transaction.
        client_offered (Optional[Union[UUID, UserBase]]): The user who offered the transaction (payer).
        client_requested (Optional[Union[UUID, UserBase]]): The user who requested the transaction (payee).
        transaction_date (datetime): The date of the transaction.
        transaction_details (Optional[str]): Additional details about the transaction.
        payment_method (str): The method of payment used in the transaction.
        transaction_status (PaymentStatusEnum): The status of the transaction.
        invoice_number (str): The invoice number associated with the transaction.
    """

    transaction_type: Annotated[str, constr(max_length=50)]
    transaction_number: Optional[Annotated[str, constr(max_length=50)]] = None
    client_offered: Optional[Union[UUID, UserBase]] = None
    client_requested: Optional[Union[UUID, UserBase]] = None
    transaction_date: datetime
    transaction_details: Optional[Annotated[str, constr(max_length=255)]] = None
    payment_method: Annotated[str, constr(max_length=50)]
    transaction_status: PaymentStatus
    invoice_number: Annotated[str, constr(max_length=50)]

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        use_enum_values=True,
    )


class Transaction(TransactionBase):
    """
    Model for representing a transaction with additional details.

    Attributes:
        transaction_id (UUID): The unique identifier for the transaction.
    """

    transaction_id: UUID

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        use_enum_values=True,
    )


class TransactionCreateSchema(TransactionBase):
    """
    Schema for creating a transaction.

    Inherits from TransactionBase.
    """

    model_config = ConfigDict(from_attributes=True)


class TransactionUpdateSchema(TransactionBase):
    """
    Schema for updating a transaction.

    Inherits from TransactionBase.
    """

    model_config = ConfigDict(from_attributes=True)


class TransactionResponse(TransactionBase, UserBaseMixin):
    """
    Model for representing a transaction response.

    Attributes:
        transaction_id (UUID): The unique identifier for the transaction.
    """

    transaction_id: Optional[UUID] = None

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        use_enum_values=True,
        populate_by_name=True,
    )

    @classmethod
    def from_orm_model(cls, transaction: TransactionModel) -> "TransactionResponse":
        """
        Create a TransactionResponse instance from an ORM model.

        Args:
            transaction (TransactionModel): Transaction ORM model.

        Returns:
            TransactionResponse: Transaction response object.
        """
        return cls(
            transaction_id=transaction.transaction_id,
            transaction_number=transaction.transaction_number,
            transaction_type=transaction.transaction_type,
            client_offered=transaction.client_offered_transaction,
            client_requested=transaction.client_requested_transaction,
            transaction_date=transaction.transaction_date,
            transaction_details=transaction.transaction_details,
            payment_method=transaction.payment_method,
            transaction_status=transaction.transaction_status,
            invoice_number=transaction.invoice_number,
        ).model_dump()
