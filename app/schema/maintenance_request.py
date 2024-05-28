from enum import Enum
from uuid import UUID
from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, Field

from app.models import MaintenanceRequest as MaintenanceRequestModel
from app.schema import UserBase, Property, PropertyUnit, PropertyUnitAssoc

class MaintenanceStatusEnum(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"

class MaintenanceRequestBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: MaintenanceStatusEnum = Field(alias='status')
    priority: int = None
    requested_by: Optional[UUID | UserBase] = None
    property_unit_assoc_id: Optional[UUID | Property | PropertyUnit | Any] = None
    scheduled_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    is_emergency: bool = Field(default=False)

    class Config:
        from_attributes = True

class MaintenanceRequestCreateSchema(BaseModel):
    title: str
    description: Optional[str] = None
    status: MaintenanceStatusEnum = MaintenanceStatusEnum.pending
    priority: int = 0
    requested_by: Optional[UUID | UserBase] = None
    property_unit_assoc_id: Optional[UUID] = None
    scheduled_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    is_emergency: bool = False

    class Config:
        from_attributes = True
        use_enum_values = True
        populate_by_name = True

class MaintenanceRequestUpdateSchema(MaintenanceRequestBase):
    task_number: Optional[str] = Field("", alias='task_number')
    id: Optional[UUID] = Field(None, alias='id')

    class Config:
        from_attributes = True
        use_enum_values = True
        populate_by_name = True

class MaintenanceRequestResponse(BaseModel):
    id: Optional[UUID] = Field(None, alias='id')
    task_number: Optional[str] = Field("", alias='task_number')
    title: Optional[str] = None
    description: Optional[str] = None
    status: MaintenanceStatusEnum = Field(alias='status')
    priority: int = None
    requested_by: Optional[UUID | UserBase] = None
    property_unit_assoc: Optional[UUID | Property | PropertyUnit] = None
    scheduled_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    is_emergency: bool = Field(default=False)
    created_at: Optional[datetime]

    @classmethod
    def get_property_info(cls, property: Property):
        property : Property = property

        return Property(
            property_unit_assoc_id = property.property_unit_assoc_id,
            name = property.name,
            property_type = property.property_type.name,
            amount = property.amount,
            security_deposit = property.security_deposit,
            commission = property.commission,
            floor_space = property.floor_space,
            num_units = property.num_units,
            num_bathrooms = property.num_bathrooms,
            num_garages = property.num_garages,
            has_balconies = property.has_balconies,
            has_parking_space = property.has_parking_space,
            pets_allowed = property.pets_allowed,
            description = property.description,
            property_status = property.property_status,
        )
    
    @classmethod
    def get_property_unit_info(cls, property_unit: PropertyUnit):
        property_unit : PropertyUnit = property_unit

        return PropertyUnit(
            property_unit_assoc_id = property_unit.property_unit_assoc_id,
            property_unit_code = property_unit.property_unit_code,
            property_unit_floor_space = property_unit.property_unit_floor_space,
            property_unit_amount = property_unit.property_unit_amount,
            property_floor_id = property_unit.property_floor_id,
            property_unit_notes = property_unit.property_unit_notes,
            has_amenities = property_unit.has_amenities,
            property_id = property_unit.property_id,
            property_unit_security_deposit = property_unit.property_unit_security_deposit,
            property_unit_commission = property_unit.property_unit_commission
        )
    
    @classmethod
    def get_property_unit_assoc(cls, property_unit_assoc: PropertyUnitAssoc):

        if property_unit_assoc.property_unit_type == "Units":
            property_unit_assoc = cls.get_property_unit_info(property_unit_assoc)
        else:
            property_unit_assoc = cls.get_property_info(property_unit_assoc)
            
        return property_unit_assoc

    @classmethod
    def from_orm_model(cls, maintenance_request: MaintenanceRequestModel):

        result = cls(
            id=maintenance_request.id,
            task_number=maintenance_request.task_number,
            title=maintenance_request.title,
            description=maintenance_request.description,
            status=maintenance_request.status,
            priority=maintenance_request.priority,
            requested_by=maintenance_request.user,
            property_unit_assoc=cls.get_property_unit_assoc(maintenance_request.prop_assoc),
            scheduled_date=maintenance_request.scheduled_date,
            completed_date=maintenance_request.completed_date,
            is_emergency=maintenance_request.is_emergency,
            created_at =maintenance_request.created_at
        ).model_dump()

        return result