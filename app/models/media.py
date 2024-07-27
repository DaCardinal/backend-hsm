import uuid
from sqlalchemy import Column, String, UUID, Boolean

from app.models.model_base import BaseModel as Base


class Media(Base):
    __tablename__ = "media"

    media_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4,
    )
    media_name = Column(String(128))
    media_type = Column(String(50))
    content_url = Column(String(500))
    is_thumbnail = Column(Boolean, default=False)
