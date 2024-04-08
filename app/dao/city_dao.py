from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Type, Optional

from app.dao.base_dao import BaseDAO
from app.models import City

class CityDAO(BaseDAO[City]):
    def __init__(self, model: Type[City]):
        super().__init__(model)