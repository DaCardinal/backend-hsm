from app.dao.resources.base_dao import BaseDAO
from app.models.transaction_type import TransactionType


class TransactionTypeDAO(BaseDAO[TransactionType]):
    def __init__(self, excludes=[], nesting_degree: str = BaseDAO.NO_NESTED_CHILD):
        self.model = TransactionType
        self.primary_key = "transaction_type_name"

        super().__init__(self.model, nesting_degree=nesting_degree, excludes=excludes)
