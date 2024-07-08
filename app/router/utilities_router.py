from typing import List

from app.schema import UtilitiesSchema
from app.dao.utilities_dao import UtilitiesDAO
from app.router.base_router import BaseCRUDRouter

class UtilitiesRouter(BaseCRUDRouter):

    def __init__(self, prefix: str = "", tags: List[str] = []):
        self.dao : UtilitiesDAO = UtilitiesDAO(nesting_degree=BaseCRUDRouter.NO_NESTED_CHILD, excludes=[''])

        super().__init__(dao=self.dao, schemas=UtilitiesSchema, prefix=prefix,tags = tags)
        self.register_routes()

    def register_routes(self):
        pass
