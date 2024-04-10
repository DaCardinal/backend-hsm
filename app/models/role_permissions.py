from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.models.model_base import BaseModel as Base


class RolePermissions(Base):
    __tablename__ = 'role_permissions'
    role_id = Column(UUID(as_uuid=True), ForeignKey('role.role_id'), primary_key=True)
    permission_id = Column(UUID(as_uuid=True), ForeignKey('permissions.permission_id'), primary_key=True)