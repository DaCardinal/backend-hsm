import uuid
from sqlalchemy import Column, String, UUID
from sqlalchemy.orm import relationship

from app.models.model_base import BaseModel


# TODO: Decide if to remove relationship to utilities and warnings
# Suppress specific SQLAlchemy warnings
# warnings.filterwarnings(
#     "ignore",
#     category=SAWarning,
#     message=r"^Expression.*is marked as 'remote', but these column\(s\) are local to the local side.*"
# )
class PropertyUnitAssoc(BaseModel):
    __tablename__ = "property_unit_assoc"

    property_unit_assoc_id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    property_unit_type = Column(String)

    __mapper_args__ = {
        "polymorphic_on": property_unit_type,
        "polymorphic_identity": "property_unit_assoc",
    }

    units = relationship(
        "Property",
        primaryjoin="and_(PropertyUnitAssoc.property_unit_type == 'Property', Property.property_unit_assoc_id == PropertyUnitAssoc.property_unit_assoc_id)",
        foreign_keys="[Property.property_unit_assoc_id]",
        remote_side="[PropertyUnitAssoc.property_unit_assoc_id]",
        lazy="selectin",
        viewonly=True,
    )

    property = relationship(
        "Units",
        primaryjoin="and_(PropertyUnitAssoc.property_unit_type == 'Units', Units.property_unit_assoc_id == PropertyUnitAssoc.property_unit_assoc_id)",
        foreign_keys="[Units.property_unit_assoc_id]",
        remote_side="[PropertyUnitAssoc.property_unit_assoc_id]",
        lazy="selectin",
        viewonly=True,
    )

    members = relationship(
        "User",
        secondary="under_contract",
        primaryjoin="and_(PropertyUnitAssoc.property_unit_assoc_id == UnderContract.property_unit_assoc_id)",
        secondaryjoin="and_(UnderContract.client_id == User.user_id)",
        foreign_keys="[UnderContract.property_unit_assoc_id, UnderContract.client_id]",
        overlaps="client_representative, properties",
    )

    # relationship to assignments
    assignments = relationship(
        "User", secondary="property_assignment", back_populates="property"
    )

    # relationship to utilities
    # utilities = relationship("Utilities",
    #                      secondary="entity_utilities",
    #                      primaryjoin="and_(EntityUtilities.property_unit_assoc_id==PropertyUnitAssoc.property_unit_assoc_id)",
    #                      lazy='selectin')

    # relationship to amenities
    amenities = relationship(
        "Amenities",
        secondary="entity_amenities",
        primaryjoin="and_(EntityAmenities.entity_assoc_id==PropertyUnitAssoc.property_unit_assoc_id)",
        overlaps="ammenities",
    )

    # relationship to message recipients
    messages_recipients = relationship(
        "MessageRecipient", back_populates="message_group", lazy="selectin"
    )

    # relationship to contracts
    under_contract = relationship(
        "UnderContract",
        back_populates="properties",
        overlaps="members",
        lazy="selectin",
    )

    prop_maintenance_requests = relationship(
        "MaintenanceRequest",
        back_populates="property_unit_assoc",
        cascade="save-update, merge",
        foreign_keys="MaintenanceRequest.property_unit_assoc_id",
    )

    prop_unit_assoc_tours = relationship(
        "Tour",
        back_populates="property_unit_assoc",
        cascade="save-update, merge",
        foreign_keys="Tour.property_unit_assoc_id",
    )
