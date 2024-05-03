from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Type
from typing_extensions import override

from app.dao.base_dao import BaseDAO
from app.dao.property_unit_assoc_dao import PropertyUnitAssocDAO
from app.models import Units, PropertyUnitAssoc
from app.utils.response import DAOResponse
from app.schema import PropertyUnitCreateSchema, PropertyUnitResponse, PropertyUnitBase


class PropertyUnitDAO(BaseDAO[Units]):
    def __init__(self, model: Type[Units]):
        super().__init__(model)
        self.property_unit_assoc_dao = PropertyUnitAssocDAO(PropertyUnitAssoc)

    @override
    async def create(self, db_session: AsyncSession, obj_in: PropertyUnitCreateSchema) -> DAOResponse:

        try:
            # get the entity dump info
            entity_data : dict = obj_in

            # extract base information
            property_unit_info : PropertyUnitCreateSchema = self.extract_model_data(obj_in, PropertyUnitBase)
            new_property_unit : Units = await super().create(db_session=db_session, obj_in=property_unit_info)
            
            # Link user model to new addresses
            await self.property_unit_assoc_dao.create(db_session = db_session, obj_in = {
                "property_id": entity_data.get('property_id'),
                "property_unit_id": new_property_unit.property_unit_id
            })
            
            # commit object to db session
            await self.commit_and_refresh(db_session, new_property_unit)
            return DAOResponse[PropertyUnitResponse](success=True, data=new_property_unit.to_dict())
        except Exception as e:
            await db_session.rollback()
            return DAOResponse(success=False, error=f"Fatal Units {str(e)}")

