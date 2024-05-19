from typing import List

from app.models import Contract
from app.dao.contract_dao import ContractDAO
from app.schema import ContractSchema, ContractCreateSchema, ContractUpdateSchema
from app.router.base_router import BaseCRUDRouter

class ContractRouter(BaseCRUDRouter):

    def __init__(self, dao: ContractDAO = ContractDAO(Contract, load_parent_relationships=False, load_child_relationships=False), prefix: str = "", tags: List[str] = []):
        self.dao = dao
        ContractSchema["create_schema"] = ContractCreateSchema
        ContractSchema["update_schema"] = ContractUpdateSchema
        super().__init__(dao=dao, schemas=ContractSchema, prefix=prefix,tags = tags)
        self.register_routes()

    def register_routes(self):
        pass
