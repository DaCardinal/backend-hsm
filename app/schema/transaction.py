from enum import Enum
from uuid import UUID
from decimal import Decimal
from datetime import datetime
from typing import List, Optional, Any
from pydantic import BaseModel, Field

from app.models import Transaction as TransactionModel, User
from app.schema import UserBase

class PaymentStatusEnum(str, Enum):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"

class TransactionBase(BaseModel):
    transaction_type_id: str
    client_offered: Optional[UserBase]  # payer_id
    client_requested: Optional[UserBase]  # payee_id
    transaction_date: datetime
    transaction_details: Optional[str]
    payment_method: str
    transaction_status: PaymentStatusEnum
    invoice_number: str

    class Config:
        from_attributes = True
        use_enum_values = True
        populate_by_name = True

class Transaction(TransactionBase):
    transaction_id: UUID

    class Config:
        from_attributes = True
        use_enum_values = True
        populate_by_name = True

class TransactionCreateSchema(TransactionBase):
    pass

class TransactionUpdateSchema(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    transaction_id: UUID

    class Config:
        from_attributes = True
        use_enum_values = True
        populate_by_name = True
        arbitrary_types_allowed=True

    @classmethod
    def get_user_info(cls, user: User):

        return User(
            first_name=user.first_name,
            last_name=user.last_name,
            photo_url=user.photo_url,
            email=user.email
        )
        
    @classmethod
    def from_orm_model(cls, transaction: TransactionModel):
        
        result = cls(
            transaction_id = transaction.transaction_id,
            transaction_type_id = transaction.transaction_type_id,
            client_offered = transaction.client_offered_transaction,
            client_requested = transaction.client_requested_transaction,
            transaction_date = transaction.transaction_date,
            transaction_details = transaction.transaction_details,
            payment_method = transaction.payment_method,
            transaction_status = transaction.transaction_status.name,
            invoice_number = transaction.invoice_number
        ).model_dump()

        return result