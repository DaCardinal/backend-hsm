from typing import Type

from app.dao.base_dao import BaseDAO
from app.models import Region

class RegionDAO(BaseDAO[Region]):
    def __init__(self, model: Type[Region]):
        super().__init__(model)