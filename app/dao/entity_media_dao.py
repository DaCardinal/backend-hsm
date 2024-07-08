from typing import Dict, Union
from typing_extensions import override
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import EntityMedia
from app.dao.base_dao import BaseDAO
from app.utils.response import DAOResponse
from app.schema import EntityMediaCreateSchema
from app.models.entity_media import EntityMedia

class EntityMediaDAO(BaseDAO[EntityMedia]):
    def __init__(self):
        self.model = EntityMedia

        super().__init__(self.model)

    @override
    async def create(self, db_session: AsyncSession, obj_in: Union[EntityMediaCreateSchema | Dict], media_store: str = None) -> DAOResponse:
        try:
            # specify calling class
            media_store = self.model.__name__ if media_store is None else media_store

            # extract base information
            entity_media_info = self.extract_model_data(obj_in, EntityMediaCreateSchema)
            entity_media = await super().create(db_session=db_session, obj_in=entity_media_info) 
            
            return DAOResponse(success=True, data=entity_media)
        except Exception as e:
            await db_session.rollback()
            return DAOResponse(success=False, error=f"{str(e)}")