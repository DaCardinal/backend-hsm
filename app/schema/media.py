from uuid import UUID
from pydantic import BaseModel, ConfigDict, constr
from typing import Annotated, Optional


class EntityMediaCreateSchema(BaseModel):
    """
    Schema for creating an entity media association.

    Attributes:
        entity_media_id (Optional[UUID]): The unique identifier for the entity media association.
        entity_type (str): The type of the entity.
        media_id (UUID): The unique identifier for the media.
        media_assoc_id (UUID): The unique identifier for the media association.
    """

    entity_media_id: Optional[UUID] = None
    entity_type: Annotated[str, constr(max_length=50)]
    media_id: UUID
    media_assoc_id: UUID

    model_config = ConfigDict(from_attributes=True)


class MediaBase(BaseModel):
    """
    Base model for media information.

    Attributes:
        media_name (str): The name of the media.
        media_type (str): The type of the media.
        content_url (str): The URL where the media content is located.
    """

    media_name: str
    media_type: str
    content_url: str
    is_thumbnail: Optional[bool] = None
    caption: Optional[str] = None
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class Media(BaseModel):
    """
    Model for representing media with additional details.

    Attributes:
        media_id (UUID): The unique identifier for the media.
    """

    media_id: UUID
    media_name: str
    media_type: str
    content_url: str
    is_thumbnail: Optional[bool] = None
    caption: Optional[str] = None
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class MediaCreateSchema(BaseModel):
    """
    Schema for creating new media.

    Attributes:
        media_name (str): The name of the media.
        media_type (str): The type of the media.
        content_url (str): The URL where the media content is located.
    """

    media_name: str
    media_type: str
    content_url: str
    is_thumbnail: Optional[bool]
    caption: Optional[str] = None
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class MediaUpdateSchema(MediaBase):
    """
    Schema for updating media information.

    Attributes:
        media_name (str): The name of the media.
        media_type (str): The type of the media.
        content_url (str): The URL where the media content is located.
    """

    media_id: UUID
    media_name: str
    media_type: str
    content_url: str
    is_thumbnail: Optional[bool]
    caption: Optional[str] = None
    description: Optional[str] = None

    # TODO: Add media_id to MediaUpdateSchema
    model_config = ConfigDict(from_attributes=True)


class MediaResponse(Media):
    """
    Schema for representing a media response.

    Attributes:
        media_id (Optional[UUID]): The unique identifier for the media.
        media_name (str): The name of the media.
        media_type (str): The type of the media.
        content_url (str): The URL where the media content is located.
    """

    media_id: Optional[UUID] = None
    media_name: Annotated[str, constr(max_length=255)]
    media_type: Annotated[str, constr(max_length=50)]
    content_url: Annotated[str, constr(max_length=255)]
    is_thumbnail: Optional[bool]
    caption: Optional[str] = None
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    @classmethod
    def from_orm_model(cls, media: Media) -> "MediaResponse":
        """
        Create a MediaResponse instance from an ORM model.

        Args:
            media (MediaModel): Media ORM model.

        Returns:
            MediaResponse: Media response object.
        """
        return cls(
            media_id=media.media_id,
            media_name=media.media_name,
            media_type=media.media_type,
            content_url=media.content_url,
            is_thumbnail=media.is_thumbnail,
            caption=media.caption,
            description=media.description,
        ).model_dump()
