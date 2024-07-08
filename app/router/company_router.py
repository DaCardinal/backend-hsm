from typing import List

from app.models import Company
from app.schema import CompanySchema
from app.dao.company_dao import CompanyDAO
from app.router.base_router import BaseCRUDRouter

class CompanyRouter(BaseCRUDRouter):

    def __init__(self, prefix: str = "", tags: List[str] = []):
        self.dao : CompanyDAO = CompanyDAO(nesting_degree=BaseCRUDRouter.NO_NESTED_CHILD, excludes=[''])

        super().__init__(dao=self.dao, schemas=CompanySchema, prefix=prefix,tags = tags)
        self.register_routes()

    def register_routes(self):
        pass
