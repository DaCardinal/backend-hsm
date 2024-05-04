import uuid
from sqlalchemy import Column, ForeignKey, Boolean, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.model_base import BaseModel as Base

class UnitsAmenities(Base):
    __tablename__ = 'units_amenities'
    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True, default=uuid.uuid4)
    amenity_id = Column(UUID(as_uuid=True), ForeignKey('amenities.amenity_id'))
    property_unit_assoc_id = Column(UUID(as_uuid=True), ForeignKey('property_unit_assoc.property_unit_assoc_id'))
    apply_to_units = Column(Boolean, default=False)
    # amenity_value = Column(String(128))
    # amenity_value_type = Column(String(50))

    ammenities = relationship('Amenities', lazy="selectin")
