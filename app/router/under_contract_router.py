from typing import List

from app.router.base_router import BaseCRUDRouter
from app.dao.contracts.under_contract_dao import UnderContractDAO

# schemas
from app.schema.schemas import UnderContractSchema
from app.schema.under_contract import UnderContractCreate, UnderContractUpdate


class UnderContractRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        # initialize router dao
        UnderContractSchema["create_schema"] = UnderContractCreate
        UnderContractSchema["update_schema"] = UnderContractUpdate

        self.dao: UnderContractDAO = UnderContractDAO(
            nesting_degree=BaseCRUDRouter.NO_NESTED_CHILD, excludes=[""]
        )

        super().__init__(
            dao=self.dao, schemas=UnderContractSchema, prefix=prefix, tags=tags
        )
        self.register_routes()

    def register_routes(self):
        pass
