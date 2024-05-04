from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import selectinload
from typing import List, Optional, Type, Union

from app.dao.base_dao import BaseDAO
from app.models import Media as MediaModel
from app.dao.entity_media_dao import EntityMediaDAO
from app.models import EntityMedia
from app.schema import MediaBase, Media

class MediaDAO(BaseDAO[MediaModel]):
    def __init__(self, model: Type[MediaModel]):
        super().__init__(model)
        self.primary_key = "media_id"

    async def add_entity_media(self, db_session: AsyncSession, property_id: str, media_info: Union[Media | MediaBase | List[Media] | List[MediaBase]], entity_model=None) -> Optional[Media | MediaBase | List[Media] | List[MediaBase]]:
        try:
            entity_media_dao = EntityMediaDAO(EntityMedia)
            results = []

            if not isinstance(media_info, list):
                media_info = [media_info]

            for media_item in media_info:
                media_item : Media = media_item

                # Check if the address already exists
                existing_media_item = await self.query(db_session=db_session, filters={f"{self.primary_key}": media_item.media_id}, single=True, options=[selectinload(MediaModel.properties_units)]) if self.primary_key in media_item.model_fields else None

                if existing_media_item:
                        # Update the existing address
                        obj_data = self.extract_model_data(media_item.model_dump(), Media)
                        media_data = Media(**obj_data)

                        create_media_item : MediaModel = await self.update(db_session=db_session, db_obj=existing_media_item, obj_in=media_data)
                else :
                    create_media_item : Media = await self.query(db_session=db_session, filters={**media_item.model_dump()}, single=True)
                    
                    if create_media_item is None:
                        create_media_item : Media = await self.create(db_session=db_session, obj_in=media_item.model_dump())

                    await entity_media_dao.create(db_session=db_session, obj_in={
                        "entity_type":  entity_model if entity_model else self.model.__name__,
                        "entity_id": property_id,
                        "media_id": create_media_item.media_id
                    })
                results.append(create_media_item)

            return results
        except NoResultFound:
            pass