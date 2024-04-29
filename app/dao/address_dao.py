from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict, Type, override

from app.dao.base_dao import BaseDAO
from app.dao.addr_country_dao import CountryDAO
from app.dao.addr_region_dao import RegionDAO
from app.dao.addr_city_dao import CityDAO
from app.models import Addresses, City, Country, Region
from app.schema import AddressCreateSchema

class AddressDAO(BaseDAO[Addresses]):
    def __init__(self, model: Type[Addresses]):
        super().__init__(model)

    async def _get_location_info(self, db_session: AsyncSession, address_data: AddressCreateSchema) -> AddressCreateSchema:
        country_dao = CountryDAO(Country)
        region_dao = RegionDAO(Region)
        city_dao = CityDAO(City)

        country : Country = await country_dao.query_on_create(db_session=db_session, filters={'country_name': address_data.country}, single=True, create_if_not_exist=True)
        region : Region = await region_dao.query_on_create(db_session=db_session, filters={'country_id': country.country_id, 'region_name': address_data.region}, single=True, create_if_not_exist=True)
        city : City = await city_dao.query_on_create(db_session=db_session, filters={'region_id': region.region_id, 'city_name': address_data.city}, single=True, create_if_not_exist=True)
        
        # set address data
        address_data.country = country
        address_data.region = region
        address_data.city = city

        return address_data

    @override
    async def create(self, db_session: AsyncSession, address_data: AddressCreateSchema):
        address_data = await self._get_location_info(db_session, address_data)

        address_data.address_type = address_data.address_type.value
        result = await super().create(db_session=db_session, obj_in={**address_data.model_dump()})

        return result if result else None

    @override
    async def update(self, db_session: AsyncSession, db_obj: Addresses, obj_in: Dict[str, Any]):
        address_data = AddressCreateSchema(**obj_in)
        address_data = await self._get_location_info(db_session, address_data)


        address_data.address_type = address_data.address_type.value
        result = await super().update(db_session=db_session, db_obj=db_obj, obj_in=address_data)
        await self.commit_and_refresh(db_session, result)

        return result if result else None