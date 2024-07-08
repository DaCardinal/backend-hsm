from typing import Type

from app.dao.base_dao import BaseDAO
from app.models import InvoiceItem

class InvoiceItemDAO(BaseDAO[InvoiceItem]):
    def __init__(self, excludes = [], nesting_degree : str = BaseDAO.NO_NESTED_CHILD):
        self.model = InvoiceItem
        self.primary_key = "invoice_item_id"
       
        super().__init__(self.model, nesting_degree = nesting_degree, excludes=excludes)