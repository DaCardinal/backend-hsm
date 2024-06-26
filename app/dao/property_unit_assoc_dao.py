from typing import Type

from app.dao.base_dao import BaseDAO
from app.models import PropertyUnitAssoc

class PropertyUnitAssocDAO(BaseDAO[PropertyUnitAssoc]):
    def __init__(self, model: Type[PropertyUnitAssoc]):
        super().__init__(model)