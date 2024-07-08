from typing import List

from app.schema import TransactionTypeSchema
from app.router.base_router import BaseCRUDRouter
from app.dao.transaction_type_dao import TransactionTypeDAO

class TransactionTypeRouter(BaseCRUDRouter):

    def __init__(self, prefix: str = "", tags: List[str] = []):
        self.dao : TransactionTypeDAO = TransactionTypeDAO(nesting_degree=BaseCRUDRouter.NO_NESTED_CHILD, excludes=[''])

        super().__init__(dao=self.dao, schemas=TransactionTypeSchema, prefix=prefix,tags = tags)
        self.register_routes()

    def register_routes(self):
        pass