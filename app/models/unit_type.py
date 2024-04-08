from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.model_base import BaseModel as Base

class UnitType(Base):
    __tablename__ = 'unit_type'
    unit_type_id = Column(UUID(as_uuid=True), primary_key=True)
    unit_type_name = Column(String(128))

    units = relationship('Units', back_populates='unit_type')