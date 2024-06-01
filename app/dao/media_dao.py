import re
import uuid
import cloudinary
import cloudinary.api
import cloudinary.uploader
from pydantic import ValidationError
from typing_extensions import override
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, List, Dict, Optional, Type, Union

from app.utils import settings
from app.dao.base_dao import BaseDAO
from app.utils.response import DAOResponse
from app.dao.entity_media_dao import EntityMediaDAO
from app.models import Media as MediaModel, EntityMedia
from app.schema import MediaBase, Media, MediaCreateSchema, MediaResponse, MediaUpdateSchema

class MediaDAO(BaseDAO[MediaModel]):
    def __init__(self, model: Type[MediaModel], load_parent_relationships: bool = False, load_child_relationships: bool = False, excludes = []):
        super().__init__(model, load_parent_relationships, load_child_relationships, excludes)
        self.primary_key = "media_id"

    @override
    async def create(self, db_session: AsyncSession, obj_in: Union[MediaCreateSchema | Dict], media_store: str = None) -> DAOResponse:
        try:
            # specify calling class
            media_store = self.model.__name__ if media_store is None else media_store

            # extract base information
            media_info = self.extract_model_data(obj_in, MediaCreateSchema)

            # upload base64 image to cloudinary and get url
            base64_data = media_info.get('content_url')
            upload_response = self.upload_to_cloudinary(base64_image=base64_data, file_name=media_info.get('media_name'), media_type=media_store.lower())
            
            # check for content url succes
            if upload_response.success == False:
                raise Exception(str(upload_response.error))
            
            media_info['content_url'] = upload_response.data['content_url'] if upload_response.success else None

            # determine image_type
            media_type = self.get_image_type(base64_data)
            media_info['media_type'] = media_info.get('media_type') + "_" +  media_type

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
            upload_response = self.upload_to_cloudinary(base64_image=base64_data, file_name=media_info.get('media_name'), media_type=media_store.lower())
            
            # check for content url succes
            if upload_response.success == False:
                raise Exception(str(upload_response.error))
            
            media_info['content_url'] = upload_response.data['content_url'] if upload_response.success else None

            # determine image_type
            media_type = self.get_image_type(base64_data)
            media_info['media_type'] = media_info.get('media_type') + "_" +  media_type

            # update media info
            existing_media : Media = await super().update(db_session=db_session, db_obj=db_obj, obj_in=MediaBase(**media_info))

            return DAOResponse[MediaResponse](success=True, data=MediaResponse.from_orm_model(existing_media))
        except ValidationError as e:
            return DAOResponse(success=False, validation_error=str(e))
        except Exception as e:
            await db_session.rollback()
            return DAOResponse[MediaResponse](success=False, error=f"{str(e)}")

    def get_image_type(self, base64_image: str):
        """
        Extracts the image type from a base64 encoded image string.

        Args:
            base64_image (str): The base64 encoded image string.

        Returns:
            str: The image type (e.g., 'jpeg', 'png', 'gif') or None if not found.
        """
        # use regex to find the image type
        match = re.match(r'data:image/(?P<type>.+?);base64,', base64_image)
        if match:
            return match.group('type')
        return None

    def check_filename_exists(self, file_name: str):
        try:
            result = cloudinary.api.resources(type='upload', prefix=file_name)
            resources = result.get('resources', [])
            
            # check if the filename exists
            for resource in resources:
                if resource['public_id'] == file_name:
                    return True
            return False
        except Exception as e:
            print(f"Error checking file_name: {e}")
            return False
        
    def upload_to_cloudinary(self, base64_image: str,  file_name: str, media_type: str = "general"):
        # specify folder name
        folder_name = str(settings.APP_NAME + "/" + media_type + "/").lower()
        
        # replace spaces with underscore
        file_name = re.sub(r'\s+', '_', file_name)

        # TODO: Implement searching image information and returning it if already exists
        if self.check_filename_exists(folder_name + file_name):
            file_name = file_name + "_" + str(uuid.uuid4())

        try:
            # upload an image
            upload_result = cloudinary.uploader.upload(base64_image, resource_type="auto", public_id=file_name, folder=folder_name)

            # return upload_result['secure_url']
            return DAOResponse(success=True, data = {"content_url": upload_result['secure_url']})
        except Exception as e:
            return DAOResponse(success=False, error=f"{str(e)}")

    async def add_entity_media(self, db_session: AsyncSession, property_unit_assoc_id: str, media_info: Union[List[Media | MediaBase]  | Media | MediaBase], entity_model=None, entity_assoc_id=None) -> Optional[List[Media | MediaBase] | Media | MediaBase]:
        try:
            entity_media_dao = EntityMediaDAO(EntityMedia)
            results = []

            if not isinstance(media_info, list):
                media_info = [media_info]

            for media_item in media_info:
                media_item : Media = media_item

                # Check if the entity already exists
                existing_media_item = await self.query(db_session=db_session, filters={f"{self.primary_key}": media_item.media_id}, single=True) if self.primary_key in media_item.model_fields else None
                
                if existing_media_item:
                        obj_data = self.extract_model_data(media_item.model_dump(), Media)
                        media_data = Media(**obj_data)

                        media_upload : DAOResponse = await self.update(db_session=db_session, db_obj=existing_media_item, obj_in=media_data)

                        # check for content url succes
                        if media_upload.success == False:
                            raise Exception(str(media_upload.error))

                        await entity_media_dao.create(db_session=db_session, obj_in={
                            "entity_type":  entity_model if entity_model else self.model.__name__,
                            "media_assoc_id": entity_assoc_id if entity_assoc_id else property_unit_assoc_id,
                            "media_id": media_upload.data.media_id
                        })
                else :
                    media_upload : Media = await self.query(db_session=db_session, filters={**media_item.model_dump()}, single=True)
                    entity_model_name = entity_model if entity_model else self.model.__name__
                    
                    if media_upload is None:
                        media_upload : MediaResponse = await self.create(db_session=db_session, obj_in=media_item.model_dump(), media_store=entity_model_name.lower())

                        # check for content url succes
                        if media_upload.success == False:
                            raise Exception(str(media_upload.error))

                        entity_media_item = await entity_media_dao.create(db_session=db_session, obj_in={
                            "entity_type":  entity_model_name,
                            "media_assoc_id": entity_assoc_id if entity_assoc_id else property_unit_assoc_id,
                            "media_id": media_upload.data.media_id
                        })

                    # commit object to db session
                    await self.commit_and_refresh(db_session, entity_media_item)
                results.append(media_upload)

            return results
        except NoResultFound:
            pass
        except Exception as e:
            await db_session.rollback()
            return DAOResponse(success=False, error=f"{str(e)}")