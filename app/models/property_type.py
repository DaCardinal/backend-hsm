from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Text, UUID

from app.models.model_base import BaseModel as Base

class PropertyType(Base):
    __tablename__ = 'property_type'
    
    property_type_id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(128))
    description = Column(Text)