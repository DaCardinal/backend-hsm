from typing import List

from app.models import TransactionType
from app.dao.transaction_type_dao import TransactionTypeDAO
from app.schema import TransactionTypeSchema
from app.router.base_router import BaseCRUDRouter

class TransactionTypeRouter(BaseCRUDRouter):

    def __init__(self, dao: TransactionTypeDAO = TransactionTypeDAO(TransactionType, load_parent_relationships=False, load_child_relationships=False), prefix: str = "", tags: List[str] = []):
        self.dao = dao
        super().__init__(dao=dao, schemas=TransactionTypeSchema, prefix=prefix, tags=tags)
        self.register_routes()

    def register_routes(self):
        pass
