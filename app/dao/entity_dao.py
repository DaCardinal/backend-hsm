from typing import Type, Optional

from app.dao.base_dao import BaseDAO
from app.models.entity_address import EntityAddress

class EntityDAO(BaseDAO[EntityAddress]):
    def __init__(self, model: Type[EntityAddress]):
        super().__init__(model)

    async def add_entity_address(self, city_name: str) -> Optional[EntityAddress]:
        pass