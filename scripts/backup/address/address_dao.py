from uuid import UUID
from typing_extensions import override
from sqlalchemy.orm import selectinload
from typing import Any, Dict, Optional, Union
from sqlalchemy.ext.asyncio import AsyncSession

# utils
from app.utils.response import DAOResponse

# daos
from app.dao.resources.base_dao import BaseDAO
from app.dao.address.addr_city_dao import CityDAO
from app.dao.address.addr_region_dao import RegionDAO
from app.dao.address.addr_country_dao import CountryDAO
from app.dao.entities.entity_address_dao import EntityAddressDAO

# models
from app.models.city import City
from app.models.region import Region
from app.models.country import Country
from app.models.address import Addresses as AddressModel

# enums
from app.schema.enums import AddressTypeEnum

# schemas
from app.schema.address import AddressCreateSchema
from app.schema.mixins.address_mixin import Address, AddressBase


class AddressDAO(BaseDAO[AddressModel]):
    def __init__(self):
        self.model = AddressModel
        self.primary_key = "address_id"

        super().__init__(self.model)

    async def _get_location_info(
        self, db_session: AsyncSession, address_data: AddressCreateSchema
    ) -> AddressCreateSchema:
        country_dao = CountryDAO()
        region_dao = RegionDAO()
        city_dao = CityDAO()

        country: Country = await country_dao.query_on_create(
            db_session=db_session,
            filters={"country_name": address_data.country},
            single=True,
            create_if_not_exist=True,
        )
        region: Region = await region_dao.query_on_create(
            db_session=db_session,
            filters={
                "country_id": country.country_id,
                "region_name": address_data.region,
            },
            single=True,
            create_if_not_exist=True,
        )
        city: City = await city_dao.query_on_create(
            db_session=db_session,
            filters={"region_id": region.region_id, "city_name": address_data.city},
            single=True,
            create_if_not_exist=True,
        )

        # set address data
        address_data.country = country
        address_data.region = region
        address_data.city = city

        return address_data

    @override
    async def create(self, db_session: AsyncSession, address_data: AddressCreateSchema):
        address_data = await self._get_location_info(db_session, address_data)
        address_data.address_type = AddressTypeEnum(address_data.address_type.value)

        result = await super().create(
            db_session=db_session, obj_in={**address_data.model_dump()}
        )

        return result if result else None

    @override
    async def update(
        self, db_session: AsyncSession, db_obj: AddressModel, obj_in: Dict[str, Any]
    ):
        address_data = AddressCreateSchema(**obj_in)
        address_data = await self._get_location_info(db_session, address_data)

        address_data.address_type = AddressTypeEnum(address_data.address_type.value)
        result = await super().update(
            db_session=db_session, db_obj=db_obj, obj_in=address_data
        )

        return result if result else None

    async def add_entity_address(
        self,
        db_session: AsyncSession,
        entity_id: UUID,
        address_obj: Union[Address, AddressBase],
        entity_model=None,
    ) -> Optional[AddressModel | dict]:
        entity_address_dao = EntityAddressDAO()

        try:
            # Check if the address already exists
            existing_address = (
                await self.query(
                    db_session=db_session,
                    filters={self.primary_key: address_obj.address_id},
                    single=True,
                    options=[selectinload(AddressModel.users)],
                )
                if self.primary_key in address_obj.model_fields
                else None
            )

            if existing_address:
                # Update the existing address
                obj_data = self.extract_model_data(address_obj.model_dump(), Address)
                addr_data = Address(**obj_data)

                address: AddressModel = await self.update(
                    db_session=db_session,
                    db_obj=existing_address,
                    obj_in=addr_data.model_dump(),
                )

                # Link user model to new addresses
                await entity_address_dao.create(
                    db_session=db_session,
                    obj_in={
                        "entity_type": entity_model
                        if entity_model
                        else self.model.__name__,
                        "entity_id": entity_id,
                        "address_id": address.address_id,
                        "emergency_address": False,
                        "emergency_address_hash": "",
                    },
                )
            else:
                # Create a new Address instance from the validated address_data
                address: AddressModel = await self.create(
                    db_session=db_session, address_data=address_obj
                )

                # Link user model to new addresses
                await entity_address_dao.create(
                    db_session=db_session,
                    obj_in={
                        "entity_type": entity_model
                        if entity_model
                        else self.model.__name__,
                        "entity_id": entity_id,
                        "address_id": address.address_id,
                        "emergency_address": False,
                        "emergency_address_hash": "",
                    },
                )
            await self.commit_and_refresh(db_session=db_session, obj=address)

            return address

        except Exception as e:
            return DAOResponse[dict](
                success=False, error=f"An unexpected error occurred {e}"
            )
