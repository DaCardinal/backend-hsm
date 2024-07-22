from typing import List

from app.schema.schemas import ContractTypeSchema
from app.router.base_router import BaseCRUDRouter
from app.dao.contract_type_dao import ContractTypeDAO


class ContractTypeRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        self.dao: ContractTypeDAO = ContractTypeDAO(
            nesting_degree=BaseCRUDRouter.NO_NESTED_CHILD, excludes=[""]
        )

        super().__init__(
            dao=self.dao, schemas=ContractTypeSchema, prefix=prefix, tags=tags
        )
        self.register_routes()

    def register_routes(self):
        pass
