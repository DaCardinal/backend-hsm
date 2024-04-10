from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.model_base import BaseModel as Base

class Permissions(Base):
    __tablename__ = 'permissions'
    permission_id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(80))
    description = Column(Text)

    roles = relationship('Role', secondary='role_permissions', back_populates='permissions')