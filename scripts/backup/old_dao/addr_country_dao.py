from app.dao.base_dao import BaseDAO
from app.models.country import Country


class CountryDAO(BaseDAO[Country]):
    def __init__(self):
        self.model = Country

        super().__init__(self.model)
