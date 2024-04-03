from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
from app.models.model_base import BaseModel as Base

class Permissions(Base):
    __tablename__ = 'permissions'
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(80))
    description = Column(Text)