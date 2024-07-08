import uuid
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Boolean, String, UUID

from app.models.model_base import BaseModel as Base

class EntityBillable(Base):
    __tablename__ = 'entity_billable'

    entity_billable_id = Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True, default=uuid.uuid4)
    payment_type_id = Column(UUID(as_uuid=True), ForeignKey('payment_types.payment_type_id'))
    entity_assoc_id = Column(UUID(as_uuid=True)) # property_unit_assoc_id, contract_id
    entity_type = Column(String(80)) # [Types: units, property, contracts]
    billable_assoc_id = Column(UUID(as_uuid=True), ForeignKey('billable_assoc.billable_assoc_id')) # maintenance_requests, utilities
    billable_type = Column(String(80)) # [Types: utilities, maintenance_requests]
    billable_amount = Column(String(128))
    apply_to_units = Column(Boolean, default=False)

    payment_type = relationship('PaymentTypes', back_populates='entity_billable', lazy='selectin')
    utility = relationship('Utilities', lazy='selectin')