import enum
import uuid
import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import event, Column, ForeignKey, DateTime, Enum, UUID, String, Integer, Text, Boolean

from app.models.model_base import BaseModel as Base

class MaintenanceStatusEnum(enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"

class MaintenanceRequest(Base):
    __tablename__ = 'maintenance_requests'

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True, default=uuid.uuid4)
    task_number = Column(String(128), unique=True, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, default=MaintenanceStatusEnum.pending, nullable=True)
    priority = Column(Integer, default=1, nullable=False)  # 1 - Low, 2 - Medium, 3 - High
    requested_by = Column(UUID(as_uuid=True), ForeignKey('users.user_id'), nullable=False)
    property_unit_assoc_id = Column(UUID(as_uuid=True), ForeignKey('property_unit_assoc.property_unit_assoc_id'), nullable=True)
    scheduled_date = Column(DateTime(timezone=True), nullable=True)
    completed_date = Column(DateTime(timezone=True), nullable=True)
    is_emergency = Column(Boolean, default=False, nullable=False)

    property = relationship("Property", 
                        secondary="property_unit_assoc", 
                        primaryjoin="MaintenanceRequest.property_unit_assoc_id == PropertyUnitAssoc.property_unit_assoc_id",
                        secondaryjoin="Property.property_unit_assoc_id == PropertyUnitAssoc.property_unit_assoc_id", 
                        back_populates="maintenance_requests", lazy="selectin")
    unit = relationship("Units", 
                        secondary="property_unit_assoc", 
                        primaryjoin="MaintenanceRequest.property_unit_assoc_id == PropertyUnitAssoc.property_unit_assoc_id",
                        secondaryjoin="Units.property_unit_assoc_id == PropertyUnitAssoc.property_unit_assoc_id", 
                        back_populates="maintenance_requests", lazy="selectin")
    prop_assoc  = relationship('PropertyUnitAssoc', lazy='selectin', overlaps="maintenance_requests,maintenance_requests,property,unit")
    user = relationship('User', back_populates='maintenance_requests', lazy='selectin')


@event.listens_for(MaintenanceRequest, 'before_insert')
def receive_before_insert(mapper, connection, target: MaintenanceRequest):
    task : dict = target.to_dict()

    if 'task_number' not in task or not task['task_number'] :
        current_time_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        setattr(target, 'task_number', f"TSK{current_time_str}")

@event.listens_for(MaintenanceRequest, 'after_insert')
def receive_after_insert(mapper, connection, target: MaintenanceRequest):
    task : dict = target.to_dict()

    if 'task_number' not in task or not task['task_number'] or not target.task_number:
        current_time_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        target.task_number = f"TSK{current_time_str}"
        connection.execute(
            target.__table__.update()
            .where(target.__table__.c.id == target.id)
            .values(task_number=target.task_number)
        )
