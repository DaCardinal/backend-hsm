from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schema.schemas import TransactionSchema
from app.router.base_router import BaseCRUDRouter
from app.dao.billing.transaction_dao import TransactionDAO


class TransactionRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        self.dao: TransactionDAO = TransactionDAO(
            nesting_degree=BaseCRUDRouter.IMMEDIATE_CHILD, excludes=[""]
        )

        super().__init__(
            dao=self.dao, schemas=TransactionSchema, prefix=prefix, tags=tags
        )
        self.register_routes()

    def register_routes(self):
        @self.router.get("/status/")
        async def transaction_status(db: AsyncSession = Depends(self.get_db)):
            transaction_status = await self.dao.get_transaction_status(db_session=db)

            if transaction_status is None:
                raise HTTPException(
                    status_code=404, detail="Error retrieving transaction status."
                )

            return transaction_status
