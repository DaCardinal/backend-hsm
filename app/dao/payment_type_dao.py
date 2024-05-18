from typing import Type

from app.dao.base_dao import BaseDAO
from app.models import PaymentTypes

class PaymentTypeDAO(BaseDAO[PaymentTypes]):
    def __init__(self, model: Type[PaymentTypes], load_parent_relationships: bool = False, load_child_relationships: bool = False, excludes = []):
        super().__init__(model, load_parent_relationships, load_child_relationships, excludes=excludes)
        self.primary_key = "payment_type_id"
