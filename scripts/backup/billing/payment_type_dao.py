from app.dao.resources.base_dao import BaseDAO
from app.models.payment_type import PaymentTypes


class PaymentTypeDAO(BaseDAO[PaymentTypes]):
    def __init__(self, excludes=[], nesting_degree: str = BaseDAO.NO_NESTED_CHILD):
        self.model = PaymentTypes
        self.primary_key = "payment_type_id"

        super().__init__(self.model, nesting_degree=nesting_degree, excludes=excludes)
