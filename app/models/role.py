from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.model_base import BaseModel as Base

class Role(Base):
    __tablename__ = 'role'
    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True)
    name = Column(String(80))
    description = Column(Text)

    users = relationship("UserRoles", back_populates="role")
    permissions = relationship("RolePermissions", back_populates="role")