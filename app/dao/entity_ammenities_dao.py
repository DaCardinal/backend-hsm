from typing import Type, Optional

from app.dao.base_dao import BaseDAO
from app.models.entity_amenities import EntityAmenities

class EntityAmmenitiesDAO(BaseDAO[EntityAmenities]):
    def __init__(self, model: Type[EntityAmenities]):
        super().__init__(model)