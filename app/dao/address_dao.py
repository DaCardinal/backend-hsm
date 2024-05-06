from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import Any, Dict, Type, Optional, Union
from typing_extensions import override

from app.dao.base_dao import BaseDAO
from app.dao.entity_dao import EntityDAO
from app.dao.addr_country_dao import CountryDAO
from app.dao.addr_region_dao import RegionDAO
from app.dao.addr_city_dao import CityDAO
from app.models import Addresses, EntityAddress, City, Country, Region
from app.schema import Address, AddressBase, AddressCreateSchema
from app.utils.response import DAOResponse

class AddressDAO(BaseDAO[Addresses]):
    def __init__(self, model: Type[Addresses]):
        super().__init__(model)
        self.primary_key = "address_id"
        
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

        return result if result else None
    
    async def add_entity_address(self, db_session: AsyncSession, entity_id: UUID, address_obj: Union[Address, AddressBase], entity_model=None) -> Optional[Addresses| dict]:
        entity_address_dao = EntityDAO(EntityAddress)

        try:
            # Check if the address already exists
            existing_address = await self.query(db_session=db_session, filters={self.primary_key: address_obj.address_id}, single=True, options=[selectinload(Addresses.users)]) if self.primary_key in address_obj.model_fields else None
            
            if existing_address:
                # Update the existing address
                obj_data = self.extract_model_data(address_obj.model_dump(), Address)
                addr_data = Address(**obj_data)
                
                address : Addresses = await self.update(db_session=db_session, db_obj=existing_address, obj_in=addr_data.model_dump())

                # Link user model to new addresses
                await entity_address_dao.create(db_session = db_session, obj_in = {
                    "entity_type": entity_model if entity_model else self.model.__name__,
                    "entity_id": entity_id,
                    "address_id": address.address_id,
                    "emergency_address": False,
                    "emergency_address_hash": ""
                })
            else:
                # Create a new Address instance from the validated address_data
                address : Addresses = await self.create(db_session=db_session, address_data=address_obj)

                # Link user model to new addresses
                await entity_address_dao.create(db_session = db_session, obj_in = {
                    "entity_type": entity_model if entity_model else self.model.__name__,
                    "entity_id": entity_id,
                    "address_id": address.address_id,
                    "emergency_address": False,
                    "emergency_address_hash": ""
                })

            return address
        
        except Exception as e:
            return DAOResponse[dict](success=False, error=f"An unexpected error occurred {e}")