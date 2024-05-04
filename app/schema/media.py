from uuid import UUID
from pydantic import BaseModel

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

class MediaCreateSchema(MediaBase):

    class Config:
        from_attributes = True
    