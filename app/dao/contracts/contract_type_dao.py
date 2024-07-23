from app.dao.resources.base_dao import BaseDAO
from app.models.contract_type import ContractType


class ContractTypeDAO(BaseDAO[ContractType]):
    def __init__(self, excludes=[], nesting_degree: str = BaseDAO.NO_NESTED_CHILD):
        self.model = ContractType
        self.primary_key = "contract_type_id"

        super().__init__(self.model, nesting_degree=nesting_degree, excludes=excludes)
