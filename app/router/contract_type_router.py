from typing import List

from app.models import ContractType
from app.dao.contract_type_dao import ContractTypeDAO
from app.schema import ContractTypeSchema
from app.router.base_router import BaseCRUDRouter

class ContractTypeRouter(BaseCRUDRouter):

    def __init__(self, dao: ContractTypeDAO = ContractTypeDAO(ContractType, load_parent_relationships=False, load_child_relationships=False), prefix: str = "", tags: List[str] = []):
        super().__init__(dao=dao, schemas=ContractTypeSchema, prefix=prefix, tags=tags)
        self.dao = dao
        self.register_routes()

    def register_routes(self):
        pass
