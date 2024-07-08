from typing import List

from app.schema import TransactionSchema
from app.router.base_router import BaseCRUDRouter
from app.dao.transaction_dao import TransactionDAO

class TransactionRouter(BaseCRUDRouter):

    def __init__(self, prefix: str = "", tags: List[str] = []):
        self.dao : TransactionDAO = TransactionDAO(nesting_degree=BaseCRUDRouter.IMMEDIATE_CHILD, excludes=[''])

        super().__init__(dao=self.dao, schemas=TransactionSchema, prefix=prefix,tags = tags)
        self.register_routes()

    def register_routes(self):
        pass
