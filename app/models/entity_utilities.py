import uuid
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Boolean, String, UUID

from app.models.model_base import BaseModel as Base

class EntityUtilities(Base):
    __tablename__ = 'entity_utilities'

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True, default=uuid.uuid4)
    utility_id = Column(UUID(as_uuid=True), ForeignKey('utilities.utility_id'))
    payment_type_id = Column(UUID(as_uuid=True), ForeignKey('payment_types.payment_type_id'))
    property_unit_assoc_id = Column(UUID(as_uuid=True), ForeignKey('property_unit_assoc.property_unit_assoc_id'))
    utility_value = Column(String(128))
    apply_to_units = Column(Boolean, default=False)

    payment_type = relationship('PaymentTypes', back_populates='entity_utilities')