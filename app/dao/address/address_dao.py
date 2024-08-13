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

        self.city_dao = CityDAO()
        self.region_dao = RegionDAO()
        self.country_dao = CountryDAO()
        self.entity_address_dao = EntityAddressDAO()

        super().__init__(self.model)

    @override
    async def create(self, db_session: AsyncSession, address_data: AddressCreateSchema):
        address_data = await self.get_location_info(db_session, address_data)

        result = await super().create(
            db_session=db_session, obj_in={**address_data.model_dump()}
        )

        return result if result else None

    @override
    async def update(
        self, db_session: AsyncSession, db_obj: AddressModel, obj_in: Dict[str, Any]
    ):
        address_data = AddressCreateSchema(**obj_in)
        address_data = await self.get_location_info(db_session, address_data)

        result = await super().update(
            db_session=db_session, db_obj=db_obj, obj_in=address_data
        )

        return result if result else None

    async def get_location_info(
        self, db_session: AsyncSession, address_data: AddressCreateSchema
    ) -> AddressCreateSchema:
        try:
            country: Country = await self.country_dao.query_on_create(
                db_session=db_session,
                filters={"country_name": address_data.country},
                single=True,
                create_if_not_exist=True,
            )
            region: Region = await self.region_dao.query_on_create(
                db_session=db_session,
                filters={
                    "country_id": country.country_id,
                    "region_name": address_data.region,
                },
                single=True,
                create_if_not_exist=True,
            )
            city: City = await self.city_dao.query_on_create(
                db_session=db_session,
                filters={"region_id": region.region_id, "city_name": address_data.city},
                single=True,
                create_if_not_exist=True,
            )

            # set address data
            address_data.city = city
            address_data.region = region
            address_data.country = country
            address_data.address_type = AddressTypeEnum(address_data.address_type.value)

        except Exception as e:
            raise Exception(str(e))

        return address_data

    async def create_or_update_address(
        self,
        db_session: AsyncSession,
        address_obj: Union[Address, AddressBase],
    ) -> AddressModel:
        """
        Creates or updates an address based on whether it already exists.
        """
        existing_address = None

        if self.primary_key in address_obj.model_fields:
            existing_address = await self.query(
                db_session=db_session,
                filters={self.primary_key: address_obj.address_id},
                single=True,
                options=[selectinload(AddressModel.users)],
            )

        if existing_address:
            obj_data = self.extract_model_data(address_obj.model_dump(), Address)
            return await self.update(
                db_session=db_session,
                db_obj=existing_address,
                obj_in=obj_data,
            )
        return await self.create(
            db_session=db_session,
            address_data=AddressCreateSchema(**address_obj.model_dump()),
        )

    async def associate_address_with_entity(
        self,
        db_session: AsyncSession,
        entity_id: UUID,
        address_id: UUID,
        entity_model: Optional[str] = None,
    ):
        """
        Associates an address with an entity (e.g., user).
        """
        await self.entity_address_dao.create(
            db_session=db_session,
            obj_in={
                "entity_type": entity_model if entity_model else self.model.__name__,
                "entity_id": entity_id,
                "address_id": address_id,
                "emergency_address": False,
                "emergency_address_hash": "",
            },
        )

    async def add_entity_address(
        self,
        db_session: AsyncSession,
        entity_id: UUID,
        address_obj: Union[Address, AddressBase],
        entity_model=None,
    ) -> Optional[AddressModel | dict]:
        try:
            # create or update the address
            address = await self.create_or_update_address(db_session, address_obj)

            # associate the address with the entity
            await self.associate_address_with_entity(
                db_session=db_session,
                entity_id=entity_id,
                address_id=address.address_id,
                entity_model=entity_model,
            )

            await self.commit_and_refresh(db_session=db_session, obj=address)

            return address

        except Exception as e:
            return DAOResponse[dict](
                success=False, error=f"An unexpected error occurred {e}"
            )
