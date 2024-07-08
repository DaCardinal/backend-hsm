import uuid
import enum
from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, ForeignKey, Enum, UUID

from app.models.model_base import BaseModel as Base

class AccountType(enum.Enum):
    asset = "asset"
    user = "user"

class UserAccounts(Base):
    __tablename__ = 'user_accounts'

    user_account_id = Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'))
    account_id = Column(UUID(as_uuid=True), ForeignKey('accounts.account_id'))