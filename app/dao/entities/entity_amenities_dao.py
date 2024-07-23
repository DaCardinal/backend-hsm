from app.dao.resources.base_dao import BaseDAO
from app.models.entity_amenities import EntityAmenities


class EntityAmenitiesDAO(BaseDAO[EntityAmenities]):
    def __init__(self):
        self.model = EntityAmenities

        super().__init__(self.model)
