from app.models import Company
from app.dao.resources.base_dao import BaseDAO


class CompanyDAO(BaseDAO[Company]):
    def __init__(self, excludes=[], nesting_degree: str = BaseDAO.NO_NESTED_CHILD):
        self.model = Company
        self.primary_key = "company_id"

        super().__init__(self.model, nesting_degree=nesting_degree, excludes=excludes)
