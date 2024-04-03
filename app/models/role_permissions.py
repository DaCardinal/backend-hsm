from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.model_base import BaseModel as Base


class RolePermissions(Base):
    __tablename__ = 'role_permissions'
    role_id = Column(UUID(as_uuid=True), ForeignKey('role.id'), primary_key=True)
    permission_id = Column(UUID(as_uuid=True), ForeignKey('permissions.id'), primary_key=True)

    permission = relationship("Permissions", back_populates="roles")