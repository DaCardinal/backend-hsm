from sqlalchemy import Column, String, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.address import Addresses
from app.models.entity_address import EntityAddress
from app.models.model_base import BaseModel as Base
from app.utils.lifespan import get_db as async_session

class Accounts(Base):
    __tablename__ = 'accounts'
    account_id = Column(UUID(as_uuid=True), primary_key=True)
    bank_account_name = Column(String(80))
    bank_account_number = Column(String(80))
    account_branch_name = Column(String(80))

    async def get_account_addresses(self):
        db_session : AsyncSession = async_session()

        async with db_session as session:
            async with session.begin():

                result = await session.execute(
                    select(Addresses).options(selectinload(Addresses.entity_addresses))
                    .join(EntityAddress, EntityAddress.address_id == Addresses.address_id)
                    .filter(EntityAddress.entity_id == self.account_id, EntityAddress.entity_type == 'account')
                )
                account_addresses = result.scalars().all()
                return account_addresses