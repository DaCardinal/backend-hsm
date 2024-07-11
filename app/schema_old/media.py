from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from app.models import Media as MediaModel

class MediaBase(BaseModel):
    media_name: str
    media_type: str
    content_url: str

    class Config:
        from_attributes = True

class Media(MediaBase):
    media_id: UUID

    class Config:
        from_attributes = True

class MediaCreateSchema(BaseModel):
    media_name: str
    media_type: str
    content_url: str

    class Config:
        from_attributes = True

class EntityMediaCreateSchema(BaseModel):
    entity_media_id: Optional[UUID] = None
    entity_type: str
    media_id: UUID
    media_assoc_id: UUID

    class Config:
        from_attributes = True

class MediaUpdateSchema(MediaBase):
    media_name: str
    media_type: str
    content_url: str

    class Config:
        from_attributes = True
    
class MediaResponse(Media):
    media_id: Optional[UUID] = None
    media_name: str
    media_type: str
    content_url: str

    class Config:
        from_attributes = True
        use_enum_values = True
    
    @classmethod
    def from_orm_model(cls, media: MediaModel):

        return cls(
            media_id = media.media_id,
            media_name = media.media_name,
            media_type = media.media_type,
            content_url = media.content_url
        ).model_dump()