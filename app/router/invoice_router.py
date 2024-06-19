from typing import List
from uuid import UUID
from fastapi import HTTPException, Depends
from fastapi import Depends, HTTPException, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Invoice
from app.dao.invoice_dao import InvoiceDAO
from app.schema import InvoiceSchema, InvoiceCreateSchema, InvoiceUpdateSchema
from app.router.base_router import BaseCRUDRouter

class InvoiceRouter(BaseCRUDRouter):

    def __init__(self, dao: InvoiceDAO = InvoiceDAO(Invoice, load_parent_relationships=True, load_child_relationships=False), prefix: str = "", tags: List[str] = [], show_default_routes=False):
        InvoiceSchema["create_schema"] = InvoiceCreateSchema
        InvoiceSchema["update_schema"] = InvoiceUpdateSchema
        super().__init__(dao=dao, schemas=InvoiceSchema, prefix=prefix, tags=tags)
        self.dao = dao
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
