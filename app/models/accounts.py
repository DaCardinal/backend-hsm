from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, UUID

from app.models.model_base import BaseModel as Base


class Accounts(Base):
    __tablename__ = "accounts"

    account_id = Column(UUID(as_uuid=True), primary_key=True)
    bank_account_name = Column(String(80))
    bank_account_number = Column(String(80))
    account_branch_name = Column(String(80))

    users = relationship(
        "User", secondary="user_accounts", back_populates="accounts", lazy="selectin"
    )
