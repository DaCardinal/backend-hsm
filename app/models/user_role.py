from sqlalchemy.orm import relationship
from sqlalchemy import UUID, Column, ForeignKey

from app.models.model_base import BaseModel as Base


class UserRoles(Base):
    __tablename__ = "user_roles"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), primary_key=True)
    role_id = Column(UUID(as_uuid=True), ForeignKey("role.role_id"), primary_key=True)

    role = relationship("Role", viewonly=True, lazy="selectin")
