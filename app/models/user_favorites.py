import uuid
from sqlalchemy.orm import relationship
from sqlalchemy import UUID, Column, String, ForeignKey

from app.models.model_base import BaseModel as Base

class FavoriteProperties(Base):
    __tablename__ = "favorite_properties"

    favorite_id = Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True, default=uuid.uuid4)
    user_id = Column(String, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    property_unit_assoc_id = Column(String, ForeignKey("property_unit_assoc.property_unit_assoc_id", ondelete="CASCADE"), primary_key=True)

    user = relationship("User", backref="favorites")
    # properties = relationship("Property", backref="favorites")