from typing import List

from app.models import Contract
from app.dao.contract_dao import ContractDAO
from app.schema import ContractSchema
from app.router.base_router import BaseCRUDRouter

class ContractRouter(BaseCRUDRouter):

    def __init__(self, dao: ContractDAO = ContractDAO(Contract, load_parent_relationships=False, load_child_relationships=False), prefix: str = "", tags: List[str] = []):
        super().__init__(dao=dao, schemas=ContractSchema, prefix=prefix, tags=tags)
        self.dao = dao
        self.register_routes()

    def register_routes(self):
        pass
