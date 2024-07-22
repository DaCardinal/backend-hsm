from sqlalchemy import Column, ForeignKey, String, UUID

from app.models.billable import BillableAssoc


class Utilities(BillableAssoc):
    __tablename__ = "utilities"

    utility_id = Column(
        UUID(as_uuid=True),
        ForeignKey("billable_assoc.billable_assoc_id"),
        primary_key=True,
    )
    name = Column(String(128))
    description = Column(String(50))

    __mapper_args__ = {
        "polymorphic_identity": "Utilities",
        "inherit_condition": utility_id == BillableAssoc.billable_assoc_id,
    }
