from typing import List

from app.models import Company
from app.dao.company_dao import CompanyDAO
from app.schema import CompanySchema
from app.router.base_router import BaseCRUDRouter

class CompanyRouter(BaseCRUDRouter):

    def __init__(self, dao: CompanyDAO = CompanyDAO(Company, load_parent_relationships=False, load_child_relationships=False), prefix: str = "", tags: List[str] = []):
        super().__init__(dao=dao, schemas=CompanySchema, prefix=prefix, tags=tags)
        self.dao = dao
        self.register_routes()

    def register_routes(self):
        pass
