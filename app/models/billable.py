import uuid
from sqlalchemy import Column, String, UUID

from app.models.model_base import BaseModel


class BillableAssoc(BaseModel):
    __tablename__ = "billable_assoc"

    billable_assoc_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    billing_type = Column(String)

    __mapper_args__ = {
        "polymorphic_on": billing_type,
        "polymorphic_identity": "billable_assoc",
    }
