from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.model_base import BaseModel as Base
from app.models.role_permissions import RolePermissions

class Role(Base):
    __tablename__ = 'role'
    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True)
    name = Column(String(80))
    alias = Column(String(80), unique=True)
    description = Column(Text)

    users = relationship('User', secondary='user_roles', back_populates='roles')
    permissions = relationship('Permissions', secondary='role_permissions', back_populates='roles')
