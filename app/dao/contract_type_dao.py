from app.models import ContractType
from app.dao.base_dao import BaseDAO

class ContractTypeDAO(BaseDAO[ContractType]):
    def __init__(self, excludes = [], nesting_degree : str = BaseDAO.NO_NESTED_CHILD):
        self.model = ContractType
        self.primary_key = "contract_type_id"

        super().__init__(self.model, nesting_degree = nesting_degree, excludes=excludes)