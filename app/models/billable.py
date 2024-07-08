import uuid
import warnings
from sqlalchemy.exc import SAWarning
from sqlalchemy import Column, String, UUID

from app.models.model_base import BaseModel

# Suppress specific SQLAlchemy warnings
warnings.filterwarnings(
    "ignore", 
    category=SAWarning, 
    message=r"^Expression.*is marked as 'remote', but these column\(s\) are local to the local side.*"
)

class BillableAssoc(BaseModel):
    __tablename__ = 'billable_assoc'

    billable_assoc_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    billing_type = Column(String)

    __mapper_args__ = {
        "polymorphic_on": billing_type,         
        "polymorphic_identity": "billable_assoc"
    }