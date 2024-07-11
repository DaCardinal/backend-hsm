from typing import List
from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, Query, Request

from app.dao.invoice_dao import InvoiceDAO
from app.router.base_router import BaseCRUDRouter

# schemas
from app.schema.schemas import InvoiceSchema
from app.schema.invoice import InvoiceCreateSchema, InvoiceUpdateSchema

class InvoiceRouter(BaseCRUDRouter):

    def __init__(self, prefix: str = "", tags: List[str] = [], show_default_routes=True):
        InvoiceSchema["create_schema"] = InvoiceCreateSchema
        InvoiceSchema["update_schema"] = InvoiceUpdateSchema
        self.dao : InvoiceDAO = InvoiceDAO(nesting_degree=BaseCRUDRouter.IMMEDIATE_CHILD, excludes=[''])

        super().__init__(dao=self.dao, schemas=InvoiceSchema, prefix=prefix,tags = tags, show_default_routes=show_default_routes)
        self.register_routes()

    def register_routes(self):
        @self.router.get("/all_lease_due/")
        async def all_lease_due(request: Request, limit: int = Query(default=10, ge=1), offset: int = Query(default=0, ge=0), db: AsyncSession = Depends(self.get_db)):
            lease = await self.dao.get_leases_due(db_session=db, offset=offset, limit=limit)

            if lease is None:
                raise HTTPException(status_code=404, detail="Error retrieving leases.")
            
            return lease
        
        @self.router.get("/user_lease_due/")
        async def user_lease_due(user_id: str, db: AsyncSession = Depends(self.get_db)):
            lease = await self.dao.get_leases_due(db_session=db, user_id=user_id)

            if lease is None:
                raise HTTPException(status_code=404, detail="Error retrieving leases.")
            
            return lease