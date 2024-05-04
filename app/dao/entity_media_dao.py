from typing import Type, Optional

from app.dao.base_dao import BaseDAO
from app.models.entity_media import EntityMedia

class EntityMediaDAO(BaseDAO[EntityMedia]):
    def __init__(self, model: Type[EntityMedia]):
        super().__init__(model)