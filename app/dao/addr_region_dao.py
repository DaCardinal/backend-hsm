from typing import Type

from app.dao.base_dao import BaseDAO
from app.models import Region

class RegionDAO(BaseDAO[Region]):
    def __init__(self):
        self.model = Region
        
        super().__init__(self.model)