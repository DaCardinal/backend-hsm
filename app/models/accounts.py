from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship, selectinload
from sqlalchemy import Column, String, select, UUID

from app.models.address import Addresses
from app.models.entity_address import EntityAddress
from app.models.model_base import BaseModel as Base
from app.utils.lifespan import get_db as async_session


class Accounts(Base):
    __tablename__ = "accounts"

    account_id = Column(UUID(as_uuid=True), primary_key=True)
    bank_account_name = Column(String(80))
    bank_account_number = Column(String(80))
    account_branch_name = Column(String(80))

    users = relationship(
        "User", secondary="user_accounts", back_populates="accounts", lazy="selectin"
    )

    async def get_account_addresses(self):
        db_session: AsyncSession = async_session()

        async with db_session as session:
            async with session.begin():
                result = await session.execute(
                    select(Addresses)
                    .options(selectinload(Addresses.entity_addresses))
                    .join(
                        EntityAddress, EntityAddress.address_id == Addresses.address_id
                    )
                    .filter(
                        EntityAddress.entity_id == self.account_id,
                        EntityAddress.entity_type == "account",
                    )
                )
                account_addresses = result.scalars().all()
                return account_addresses
