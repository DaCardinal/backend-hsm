from typing import List

from app.models import PaymentTypes
from app.dao.payment_type_dao import PaymentTypeDAO
from app.schema import PaymentTypeSchema
from app.router.base_router import BaseCRUDRouter

class PaymentTypeRouter(BaseCRUDRouter):

    def __init__(self, dao: PaymentTypeDAO = PaymentTypeDAO(PaymentTypes, load_parent_relationships=False, load_child_relationships=False), prefix: str = "", tags: List[str] = []):
        super().__init__(dao=dao, schemas=PaymentTypeSchema, prefix=prefix, tags=tags)
        self.dao = dao
        self.register_routes()

    def register_routes(self):
        pass
