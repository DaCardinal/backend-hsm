from typing import Type, Optional

from app.dao.base_dao import BaseDAO
from app.models.unit_ammenties import UnitsAmenities

class EntityAmmenitiesDAO(BaseDAO[UnitsAmenities]):
    def __init__(self, model: Type[UnitsAmenities]):
        super().__init__(model)