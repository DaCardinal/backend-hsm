from typing import Type

from app.dao.base_dao import BaseDAO
from app.models import City

class CityDAO(BaseDAO[City]):
    def __init__(self):
        self.model = City
        
        super().__init__(self.model)