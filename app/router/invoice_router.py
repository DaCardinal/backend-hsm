from typing import List

from app.models import Invoice
from app.dao.invoice_dao import InvoiceDAO
from app.schema import InvoiceSchema, InvoiceCreateSchema, InvoiceUpdateSchema
from app.router.base_router import BaseCRUDRouter

class InvoiceRouter(BaseCRUDRouter):

    def __init__(self, dao: InvoiceDAO = InvoiceDAO(Invoice, load_parent_relationships=True, load_child_relationships=False), prefix: str = "", tags: List[str] = []):
        
        self.dao = dao
        InvoiceSchema["create_schema"] = InvoiceCreateSchema
        InvoiceSchema["update_schema"] = InvoiceUpdateSchema
        super().__init__(dao=dao, schemas=InvoiceSchema, prefix=prefix, tags=tags)
        self.register_routes()

    def register_routes(self):
        pass
