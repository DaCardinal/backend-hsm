from uuid import UUID
from pydantic import ValidationError
from typing_extensions import override
from sqlalchemy.orm import selectinload
from typing import Any, Dict, List, Union
from sqlalchemy.ext.asyncio import AsyncSession

# models
from app.models.property import Property

# utils
from app.utils.response import DAOResponse

# daos
from app.dao.resources.base_dao import BaseDAO
from app.dao.resources.media_dao import MediaDAO
from app.dao.address.address_dao import AddressDAO
from app.dao.resources.utilities_dao import UtilitiesDAO
from app.dao.resources.amenities_dao import AmenitiesDAO
from app.dao.properties.property_unit_assoc_dao import PropertyUnitAssocDAO

# schemas
from app.schema.property import (
    PropertyResponse,
    PropertyBase,
    PropertyCreateSchema,
    PropertyUpdateSchema,
)


class PropertyDAO(BaseDAO[Property]):
    def __init__(self, excludes=[], nesting_degree: str = BaseDAO.NO_NESTED_CHILD):
        self.primary_key = "property_unit_assoc_id"

        self.model = Property
        self.media_dao = MediaDAO()
        self.address_dao = AddressDAO()
        self.utility_dao = UtilitiesDAO()
        self.ammenity_dao = AmenitiesDAO()
        self.property_unit_assoc_dao = PropertyUnitAssocDAO()
        self.detail_mappings = {
            "media": self.media_dao.add_entity_media,
            "amenities": self.ammenity_dao.add_entity_ammenity,
            "address": self.address_dao.add_entity_address,
            "utilities": self.utility_dao.add_entity_utility,
        }

        super().__init__(self.model, nesting_degree=nesting_degree, excludes=excludes)

    @override
    async def create(
        self, db_session: AsyncSession, obj_in: Union[PropertyCreateSchema | Dict]
    ) -> DAOResponse:
        try:
            # extract base information
            property_info = self.extract_model_data(obj_in, PropertyBase)

            # create new user
            new_property: Property = await super().create(
                db_session=db_session, obj_in=property_info
            )

            # process any entity details
            await self.handle_entity_details(
                db_session=db_session,
                entity_data=obj_in,
                detail_mappings=self.detail_mappings,
                entity_model=self.model.__name__,
                entity_assoc_id=new_property.property_unit_assoc_id,
            )

            new_load_addr: Property = await self.query(
                db_session=db_session,
                filters={f"{self.primary_key}": new_property.property_unit_assoc_id},
                single=True,
                options=[selectinload(Property.addresses)],
            )

            # commit object to db session
            await self.commit_and_refresh(db_session, new_load_addr)

            # TODO: Create a link for PropertyUnitAssoc
            return DAOResponse[PropertyResponse](
                success=True, data=PropertyResponse.from_orm_model(new_property)
            )
        except Exception as e:
            await db_session.rollback()
            return DAOResponse(success=False, error=f"Fatal {str(e)}")

    @override
    async def update(
        self, db_session: AsyncSession, db_obj: Property, obj_in: PropertyUpdateSchema
    ) -> DAOResponse[PropertyResponse]:
        try:
            # get the entity dump info
            entity_data = obj_in.model_dump()
            property_data = self.extract_model_data(
                obj_in.model_dump(
                    exclude=["address", "media", "amenities", "utilities"]
                ),
                PropertyBase,
            )

            # update property info
            existing_property: Property = await super().update(
                db_session=db_session,
                db_obj=db_obj,
                obj_in=PropertyBase(**property_data),
            )

            # process any entity details
            await self.handle_entity_details(
                db_session=db_session,
                entity_data=entity_data,
                detail_mappings=self.detail_mappings,
                entity_model=self.model.__name__,
                entity_assoc_id=existing_property.property_unit_assoc_id,
            )

            # commit object to db session
            await self.commit_and_refresh(db_session, existing_property)

            return DAOResponse[PropertyResponse](
                success=True, data=PropertyResponse.from_orm_model(existing_property)
            )

        except ValidationError as e:
            return DAOResponse(success=False, validation_error=str(e))
        except Exception as e:
            await db_session.rollback()
            return DAOResponse[PropertyResponse](
                success=False, error=f"Fatal Update {str(e)}"
            )

    @override
    async def get_all(
        self, db_session: AsyncSession, offset=0, limit=100
    ) -> DAOResponse[List[PropertyResponse]]:
        result = await super().get_all(
            db_session=db_session, offset=offset, limit=limit
        )

        if not result:
            return DAOResponse(success=True, data=[])

        return DAOResponse[List[PropertyResponse]](
            success=True, data=[PropertyResponse.from_orm_model(r) for r in result]
        )

    @override
    async def get(
        self, db_session: AsyncSession, id: Union[UUID | Any | int]
    ) -> DAOResponse[PropertyResponse]:
        result: Property = await super().get(db_session=db_session, id=id)

        if not result:
            return DAOResponse(success=True, data={})

        return DAOResponse[PropertyResponse](
            success=True, data=PropertyResponse.from_orm_model(result)
        )
