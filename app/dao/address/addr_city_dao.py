from app.models.city import City
from app.dao.resources.base_dao import BaseDAO


class CityDAO(BaseDAO[City]):
    def __init__(self):
        self.model = City

        super().__init__(self.model)
