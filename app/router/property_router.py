from uuid import UUID
from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

# utils
from app.utils import DAOResponse

# daos
from app.dao.media_dao import MediaDAO
from app.dao.property_dao import PropertyDAO

# models
from app.models import EntityMedia, Media

# routers
from app.router.base_router import BaseCRUDRouter

# schemas
from app.schema.schemas import PropertySchema
from app.schema.property import PropertyCreateSchema, PropertyUpdateSchema

class PropertyRouter(BaseCRUDRouter):

    def __init__(self, prefix: str = "", tags: List[str] = []):
        PropertySchema["create_schema"] = PropertyCreateSchema
        PropertySchema["update_schema"] = PropertyUpdateSchema
        self.dao : PropertyDAO = PropertyDAO(nesting_degree=BaseCRUDRouter.NO_NESTED_CHILD, excludes=[''])

        super().__init__(dao=self.dao, schemas=PropertySchema, prefix=prefix,tags = tags)
        self.register_routes()

    def register_routes(self):
        @self.router.post("/link_property_to_media")
        async def add_property_media(property_unit_assoc_id: UUID, media_id: UUID, db: AsyncSession = Depends(self.get_db)):
            #TODO: Implement this properly
            media_dao = MediaDAO(Media) 
            property_media : EntityMedia = await media_dao.link_entity_to_media(db_session=db, property_unit_assoc_id=property_unit_assoc_id, media_id=media_id, entity_model='Property')

            if property_media is None:
                raise HTTPException(status_code=404, detail="Error adding media to property")
            
            return DAOResponse(success=True, data=property_media.to_dict())