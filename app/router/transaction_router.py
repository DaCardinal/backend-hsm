from typing import List

from app.models import Transaction
from app.dao.transaction_dao import TransactionDAO
from app.schema import TransactionSchema
from app.router.base_router import BaseCRUDRouter

class TransactionRouter(BaseCRUDRouter):

    def __init__(self, dao: TransactionDAO = TransactionDAO(Transaction, load_parent_relationships=False, load_child_relationships=False), prefix: str = "", tags: List[str] = []):
        self.dao = dao
        super().__init__(dao=dao, schemas=TransactionSchema, prefix=prefix, tags=tags)
        self.register_routes()

    def register_routes(self):
        pass
