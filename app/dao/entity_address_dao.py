from app.dao.base_dao import BaseDAO
from app.models.entity_address import EntityAddress


class EntityAddressDAO(BaseDAO[EntityAddress]):
    def __init__(self):
        self.model = EntityAddress

        super().__init__(self.model)
