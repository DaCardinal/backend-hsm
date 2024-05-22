import uuid
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, UUID

from app.models.model_base import BaseModel as Base

class Utilities(Base):
    __tablename__ = 'utilities'
    
    utility_id = Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True, default=uuid.uuid4)
    name = Column(String(128))
    description = Column(String(50))

    units = relationship("PropertyUnitAssoc", secondary="entity_utilities", back_populates="utilities")