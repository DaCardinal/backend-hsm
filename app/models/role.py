import uuid
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Text, UUID

from app.models.model_base import BaseModel as Base

class Role(Base):
    __tablename__ = 'role'
    
    role_id = Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True, default=uuid.uuid4)
    name = Column(String(80))
    alias = Column(String(80), unique=True)
    description = Column(Text)

    users = relationship('User', secondary='user_roles', back_populates='roles') #lazy="selectin"
    permissions = relationship('Permissions', secondary='role_permissions', back_populates='roles', lazy="selectin")