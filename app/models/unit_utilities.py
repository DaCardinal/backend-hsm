from sqlalchemy import Column, ForeignKey, Boolean, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.model_base import BaseModel as Base

class UnitUtilities(Base):
    __tablename__ = 'unit_utilities'
    id = Column(UUID(as_uuid=True), primary_key=True)
    utility_id = Column(UUID(as_uuid=True), ForeignKey('utilities.utility_id'))
    payment_type_id = Column(UUID(as_uuid=True), ForeignKey('payment_types.payment_type_id'))
    property_unit_assoc = Column(UUID(as_uuid=True), ForeignKey('property_unit_assoc.property_unit_assoc'))
    utility_value = Column(String(128))
    apply_to_units = Column(Boolean, default=False)

    payment_type = relationship('PaymentTypes', back_populates='unit_utilities')