import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Type, override

from app.dao.base_dao import BaseDAO
from app.dao.addr_country_dao import CountryDAO
from app.dao.addr_region_dao import RegionDAO
from app.dao.addr_city_dao import CityDAO
from app.models import Addresses, City
from app.models.country import Country
from app.models.region import Region
from app.schema.schemas import AddressCreateSchema

class AddressDAO(BaseDAO[Addresses]):
    def __init__(self, model: Type[Addresses]):
        super().__init__(model)

    @override
    async def create(self, db_session: AsyncSession, address_data: AddressCreateSchema):
        city_dao = CityDAO(City)
        region_dao = RegionDAO(Region)
        country_dao = CountryDAO(Country)

        # check if country exists
        country_info : Country = await country_dao.query_on_create(db_session=db_session, filters={'country_name': address_data.country}, single=True, create_if_not_exist=True)
        address_data.country = country_info

        # check if region exists
        region_info : Region = await region_dao.query_on_create(db_session=db_session, filters={'country_id':country_info.country_id, 'region_name': address_data.region}, single=True, create_if_not_exist=True)
        address_data.region = region_info

        # check if city exists
        city_info : City = await city_dao.query_on_create(db_session=db_session, filters={'region_id':region_info.region_id, 'city_name': address_data.city}, single=True, create_if_not_exist=True)
        address_data.city = city_info
        
        address_data.address_type = address_data.address_type.value
        result = await super().create(db_session=db_session, obj_in={**address_data.model_dump()})

        return result if result else None