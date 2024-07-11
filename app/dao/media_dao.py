from uuid import UUID
from pydantic import ValidationError
from typing_extensions import override
from sqlalchemy.orm.exc import NoResultFound
from typing import List, Dict, Optional, Union
from sqlalchemy.ext.asyncio import AsyncSession

# models
from app.models import Media as MediaModel

# utils
from app.utils.response import DAOResponse

# services
from app.services import MediaUploaderService

# daos
from app.dao.base_dao import BaseDAO
from app.dao.entity_media_dao import EntityMediaDAO

# schemas
from app.schema.media import MediaBase, Media, MediaCreateSchema, MediaResponse, MediaUpdateSchema

class MediaDAO(BaseDAO[MediaModel]):
    def __init__(self, excludes = [], nesting_degree : str = BaseDAO.NO_NESTED_CHILD):
        self.model = MediaModel
        self.primary_key = "media_id"
        self.entity_media_dao = EntityMediaDAO()

        super().__init__(self.model, nesting_degree = nesting_degree, excludes=excludes)

    async def link_entity_to_media(self, db_session: AsyncSession, media_id: UUID, entity_assoc_id: UUID = None, entity_model=None):

        entity_media_object = {
            "entity_type":  entity_model if entity_model else self.model.__name__,
            "media_assoc_id": entity_assoc_id,
            "media_id": media_id
        }
        
        # check if entity media linkage exists
        result = await self.entity_media_dao.query(db_session=db_session, filters={**entity_media_object}, single=True)

        # create entity media linkage if it doesn't exist
        if result is None:
            result = await self.entity_media_dao.create(db_session = db_session, obj_in = entity_media_object)
        
        return []
    
    @override
    async def get_all(self, db_session: AsyncSession, offset=0, limit=100) -> DAOResponse[List[MediaResponse]]:
        result = await super().get_all(db_session=db_session, offset=offset, limit=limit)
        
        # check if no result
        if not result:
            return DAOResponse(success=True, data=[])

        return DAOResponse[List[MediaResponse]](success=True, data=[MediaResponse.from_orm_model(r) for r in result])

    @override
    async def create(self, db_session: AsyncSession, obj_in: Union[MediaCreateSchema | Dict], media_store: str = None) -> DAOResponse:
        try:
            # specify calling class
            media_store = self.model.__name__ if media_store is None else media_store

            # extract base information
            media_info = self.extract_model_data(obj_in, MediaCreateSchema)

            # upload base64 image to cloudinary and get url
            base64_data = media_info.get('content_url')
            uploader_service = MediaUploaderService(base64_image=base64_data, file_name=media_info.get('media_name'), media_type=media_store.lower())
            upload_response = uploader_service.upload()
            
            # check for content url succes
            if upload_response.success == False:
                raise Exception(str(upload_response.error))
            
            media_info['content_url'] = upload_response.data['content_url'] if upload_response.success else None

            # determine image_type
            media_type = uploader_service.get_image_type()
            media_info['media_type'] = media_type if media_type else media_info.get('media_type')

            # create new media
            new_media: Media = await super().create(db_session=db_session, obj_in=media_info)
            
            return DAOResponse[MediaResponse](success=True, data=MediaResponse.from_orm_model(new_media))
        except Exception as e:
            await db_session.rollback()
            return DAOResponse(success=False, error=f"{str(e)}")
        
    @override
    async def update(self, db_session: AsyncSession,  db_obj: Media, obj_in: MediaUpdateSchema, media_store: str = None) -> DAOResponse[MediaResponse]:
        
        try:
            # specify calling class
            media_store = self.model.__name__ if media_store is None else media_store

            # get the entity dump info
            entity_data = obj_in.model_dump()

            # extract base information
            media_info = self.extract_model_data(entity_data, Media)

            # upload base64 image to cloudinary and get url
            base64_data = media_info.get('content_url')
            uploader_service = MediaUploaderService(base64_image=base64_data, file_name=media_info.get('media_name'), media_type=media_store.lower())
            upload_response = uploader_service.upload()  

            # check for content url succes
            if upload_response.success == False:
                raise Exception(str(upload_response.error))
            
            media_info['content_url'] = upload_response.data['content_url'] if upload_response.success else None

            # determine image_type
            media_type = uploader_service.get_image_type()
            media_info['media_type'] = media_type if media_type else media_info.get('media_type')

            # update media info
            existing_media : Media = await super().update(db_session=db_session, db_obj=db_obj, obj_in=MediaBase(**media_info))

            return DAOResponse[MediaResponse](success=True, data=MediaResponse.from_orm_model(existing_media))
        except ValidationError as e:
            return DAOResponse(success=False, validation_error=str(e))
        except Exception as e:
            await db_session.rollback()
            return DAOResponse[MediaResponse](success=False, error=f"{str(e)}")

    async def add_entity_media(self, db_session: AsyncSession, property_unit_assoc_id: str, media_info: Union[List[Media | MediaBase]  | Media | MediaBase], entity_model=None, entity_assoc_id=None) -> Optional[List[Media | MediaBase] | Media | MediaBase]:
        
        try:
            results = []
            entity_model_name = entity_model if entity_model else self.model.__name__

            if not isinstance(media_info, list):
                media_info = [media_info]

            for media_item in media_info:
                media_item : Media = media_item

                # Check if the entity already exists
                existing_media_item : Media = await self.query(db_session=db_session, filters={**media_item.model_dump(exclude=["content_url"])}, single=True)

                if existing_media_item:
                    obj_data = self.extract_model_data(media_item.model_dump(), Media)
                    obj_data['media_id'] = existing_media_item.media_id
                    
                    media_data = Media(**obj_data)
                    media_upload : DAOResponse = await self.update(db_session=db_session, db_obj=existing_media_item, obj_in=media_data)
                else:
                    media_upload : MediaResponse = await self.create(db_session=db_session, obj_in=media_item.model_dump(), media_store=entity_model_name.lower())

                # check for content url succes
                if media_upload.success == False:
                    raise Exception(str(media_upload.error))
                    
                entity_media_item = await self.link_entity_to_media(
                    db_session=db_session, 
                    entity_assoc_id=entity_assoc_id if entity_assoc_id else property_unit_assoc_id,
                    media_id=media_upload.data.media_id,
                    entity_model=entity_model_name
                )

                # commit object to db session
                await self.commit_and_refresh(db_session, entity_media_item)
                results.append(media_upload)

            return results
        except NoResultFound:
            pass
        except Exception as e:
            await db_session.rollback()
            return DAOResponse(success=False, error=f"Media DAO Error: {str(e)}")