from sqlalchemy.ext.asyncio import AsyncSession
from typing import Type, overload

from app.dao.base_dao import BaseDAO
from app.dao.city_dao import CityDAO
from app.models import Addresses
from app.models.city import City
from app.schema.schemas import AddressCreateSchema

class AddressDAO(BaseDAO[Addresses]):
    def __init__(self, model: Type[Addresses]):
        super().__init__(model)

    @overload
    async def create(self, db_session: AsyncSession, address_data: AddressCreateSchema):
        city_dao = CityDAO()
        
        # check if city exists
        city_info : City = city_dao.query(db_session=db_session, filters={'city_name': address_data.city_name})

        if city_info:
            address_data.city_id = city_info.city_id
        else:
            # create new city
            new_city : City = city_dao.create(db_session=db_session, obj_in={"city_name": address_data.city_name})
            address_data.city_id = new_city.city_id
        
        return super().create(db_session=db_session, obj_in=address_data)