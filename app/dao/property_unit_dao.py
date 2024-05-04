from functools import partial
from typing import Type
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing_extensions import override

from app.dao.base_dao import BaseDAO
from app.dao.media_dao import MediaDAO
from app.dao.property_unit_assoc_dao import PropertyUnitAssocDAO
from app.models import Units, PropertyUnitAssoc, Media as MediaModel
from app.utils.response import DAOResponse
from app.schema import PropertyUnitCreateSchema, PropertyUnitUpdateSchema, PropertyUnitResponse, PropertyUnitBase, MediaBase, Media

class PropertyUnitDAO(BaseDAO[Units]):
    def __init__(self, model: Type[Units]):
        super().__init__(model)
        self.primary_key = "property_unit_id"
        self.media_dao = MediaDAO(MediaModel)
        self.property_unit_assoc_dao = PropertyUnitAssocDAO(PropertyUnitAssoc)

    @override
    async def create(self, db_session: AsyncSession, obj_in: PropertyUnitCreateSchema) -> dict:

        try:
            # get the entity dump info
            entity_data : dict = obj_in

            # extract base information
            property_unit_info : PropertyUnitCreateSchema = self.extract_model_data(obj_in, PropertyUnitBase)
            new_property_unit : Units = await super().create(db_session=db_session, obj_in=property_unit_info)
            
            # add additional info if exists
            details_methods : dict = {
                'media': (partial(self.media_dao.add_entity_media, entity_model=self.model.__name__), MediaBase)
            }
            
            if details_methods.keys() <= entity_data.keys():
                await self.process_entity_details(db_session, new_property_unit.property_unit_id, obj_in, details_methods)
                
            # Link property to property units
            await self.property_unit_assoc_dao.create(db_session = db_session, obj_in = {
                "property_id": entity_data.get('property_id'),
                "property_unit_id": new_property_unit.property_unit_id
            })
            
            # commit object to db session
            new_load_units: Units = await self.query(
                db_session=db_session,
                filters={f"{self.primary_key}":new_property_unit.property_unit_id},
                single=True,
                options=[selectinload(Units.media)]
            )
            
            # commit object to db session
            await self.commit_and_refresh(db_session, new_load_units)
            
            return DAOResponse[PropertyUnitResponse](success=True, data=PropertyUnitResponse.from_orm_model(new_load_units))
        except Exception as e:
            await db_session.rollback()
            return DAOResponse(success=False, error=f"Fatal Units {str(e)}")
        
    @override
    async def update(self, db_session: AsyncSession, db_obj: Units, obj_in: PropertyUnitUpdateSchema) -> DAOResponse[PropertyUnitResponse]:
        try:
            property_unit_data = self.extract_model_data(obj_in.model_dump(exclude=['address', 'media']), PropertyUnitBase)
            existing_property_unit = await super().update(db_session=db_session, db_obj=db_obj, obj_in=PropertyUnitBase(**property_unit_data))

            entity_data = obj_in.model_dump()
            media_schema = Media if ('media' in entity_data and entity_data['media'] and ('media_id' in entity_data['media'] or 'media_id' in entity_data['media'][0])) else MediaBase
            details_methods = {key: (partial(self.media_dao.add_entity_media, entity_model=self.model.__name__), media_schema) for key in ['media'] if key in entity_data}

            if details_methods.keys() <= entity_data.keys():
                await self.process_entity_details(db_session, existing_property_unit.property_unit_id, entity_data, details_methods)

            await self.commit_and_refresh(db_session, existing_property_unit)

            return DAOResponse[PropertyUnitResponse](success=True, data=PropertyUnitResponse.from_orm_model(existing_property_unit))
        except ValidationError as e:
            return DAOResponse(success=False, validation_error=str(e))
        except Exception as e:
            await db_session.rollback()
            return DAOResponse[PropertyUnitResponse](success=False, error=f"Fatal Update {str(e)}")