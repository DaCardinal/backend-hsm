import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict, Type, override

from app.dao.base_dao import BaseDAO
from app.dao.addr_country_dao import CountryDAO
from app.dao.addr_region_dao import RegionDAO
from app.dao.addr_city_dao import CityDAO
from app.models import Addresses, City, Country, Region
from app.schema import AddressCreateSchema
from app.utils.response import DAOResponse

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
    
    @override
    async def update(self, db_session: AsyncSession, db_obj: Addresses, obj_in: Dict[str, Any]):
        address_data : AddressCreateSchema = AddressCreateSchema(**obj_in)
        city_dao = CityDAO(City)
        region_dao = RegionDAO(Region)
        country_dao = CountryDAO(Country)
        
        city_info : City = db_obj.city
        region_info : Region = db_obj.region
        country_info : Country = db_obj.country

        try:
            # async with db_session as db:
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
            result = await super().update(db_session=db_session, db_obj=db_obj, obj_in=address_data)
            await self.commit_and_refresh(db_session, result)

            return result if result else None
        except Exception as e:
            return DAOResponse[Any](success=False, error=f"Error updating address {str(e)}")