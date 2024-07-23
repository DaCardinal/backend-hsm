from app.models.region import Region
from app.dao.base_dao import BaseDAO


class RegionDAO(BaseDAO[Region]):
    def __init__(self):
        self.model = Region

        super().__init__(self.model)
