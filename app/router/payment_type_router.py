from typing import List

from app.schema.schemas import PaymentTypeSchema
from app.router.base_router import BaseCRUDRouter
from app.dao.payment_type_dao import PaymentTypeDAO

class PaymentTypeRouter(BaseCRUDRouter):

    def __init__(self, prefix: str = "", tags: List[str] = []):
        self.dao : PaymentTypeDAO = PaymentTypeDAO(nesting_degree=BaseCRUDRouter.NO_NESTED_CHILD, excludes=[''])

        super().__init__(dao=self.dao, schemas=PaymentTypeSchema, prefix=prefix,tags = tags)
        self.register_routes()

    def register_routes(self):
        pass
