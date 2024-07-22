from typing import List
from pydantic import BaseModel, ConfigDict

from app.schema.media import Media


class MediaInfoMixin(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def get_media(cls, media_items: List[Media]) -> List[Media]:
        """
        Get media information associated with the amenity.

        Args:
            media_items (List[Media]): List of media model objects.

        Returns:
            List[Media]: List of media objects.
        """
        result = []
        for media in media_items:
            result.append(
                Media(
                    media_id=media.media_id,
                    media_name=media.media_name,
                    media_type=media.media_type,
                    content_url=media.content_url,
                    is_thumbnail=media.is_thumbnail,
                )
            )
        return result
