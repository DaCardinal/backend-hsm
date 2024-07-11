from enum import Enum
from uuid import UUID
from datetime import datetime
from typing import Any, Optional, Union, Annotated
from pydantic import BaseModel, constr

# schemas
from app.schema.user import UserBase
from app.schema.enums import MaintenanceStatus
from app.schema.property import Property, PropertyUnit, PropertyUnitAssoc

# models
from app.models import MaintenanceRequest as MaintenanceRequestModel

class MaintenanceRequestBase(BaseModel):
    """
    Base model for maintenance request information.

    Attributes:
        title (Optional[str]): The title of the maintenance request.
        description (Optional[str]): The description of the maintenance request.
        status (MaintenanceStatusEnum): The status of the maintenance request.
        priority (int): The priority of the maintenance request.
        requested_by (Optional[Union[UUID, UserBase]]): The user who requested the maintenance.
        property_unit_assoc_id (Optional[Union[UUID, Property, PropertyUnit, Any]]): The associated property unit.
        scheduled_date (Optional[datetime]): The scheduled date for the maintenance.
        completed_date (Optional[datetime]): The completed date for the maintenance.
        is_emergency (bool): Indicates if the maintenance request is an emergency.
    """
    title: Optional[Annotated[str, constr(max_length=255)]] = None
    description: Optional[Annotated[str, constr(max_length=255)]] = None
    status: MaintenanceStatus
    priority: int = 0
    requested_by: Optional[Union[UUID, UserBase]] = None
    property_unit_assoc_id: Optional[Union[UUID, Property, PropertyUnit, Any]] = None
    scheduled_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    is_emergency: bool = False

    class Config:
        from_attributes = True


class MaintenanceRequest(BaseModel):
    """
    Model for representing a maintenance request.

    Attributes:
        id (Optional[UUID]): The unique identifier for the maintenance request.
        title (Optional[str]): The title of the maintenance request.
        description (Optional[str]): The description of the maintenance request.
        status (MaintenanceStatusEnum): The status of the maintenance request.
        priority (int): The priority of the maintenance request.
        requested_by (Optional[Union[UUID, UserBase]]): The user who requested the maintenance.
        property_unit_assoc_id (Optional[Union[UUID, Property, PropertyUnit, Any]]): The associated property unit.
        scheduled_date (Optional[datetime]): The scheduled date for the maintenance.
        completed_date (Optional[datetime]): The completed date for the maintenance.
        is_emergency (bool): Indicates if the maintenance request is an emergency.
    """
    id: Optional[UUID] = None
    title: Optional[Annotated[str, constr(max_length=255)]] = None
    description: Optional[Annotated[str, constr(max_length=255)]] = None
    status: MaintenanceStatus
    priority: int = 0
    requested_by: Optional[Union[UUID, UserBase]] = None
    property_unit_assoc_id: Optional[Union[UUID, Property, PropertyUnit, Any]] = None
    scheduled_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    is_emergency: bool = False

    class Config:
        from_attributes = True


class MaintenanceRequestCreateSchema(BaseModel):
    """
    Schema for creating a maintenance request.

    Attributes:
        title (str): The title of the maintenance request.
        description (Optional[str]): The description of the maintenance request.
        status (MaintenanceStatusEnum): The status of the maintenance request.
        priority (int): The priority of the maintenance request.
        requested_by (Optional[Union[UUID, UserBase]]): The user who requested the maintenance.
        property_unit_assoc_id (Optional[UUID]): The associated property unit.
        scheduled_date (Optional[datetime]): The scheduled date for the maintenance.
        completed_date (Optional[datetime]): The completed date for the maintenance.
        is_emergency (bool): Indicates if the maintenance request is an emergency.
    """
    title: Annotated[str, constr(max_length=255)]
    description: Optional[Annotated[str, constr(max_length=255)]] = None
    status: MaintenanceStatus = MaintenanceStatus.pending
    priority: int = 0
    requested_by: Optional[Union[UUID, UserBase]] = None
    property_unit_assoc_id: Optional[UUID] = None
    scheduled_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    is_emergency: bool = False

    class Config:
        from_attributes = True
        use_enum_values = True
        populate_by_name = True


class MaintenanceRequestUpdateSchema(BaseModel):
    """
    Schema for updating a maintenance request.

    Attributes:
        task_number (Optional[str]): The task number of the maintenance request.
        id (Optional[UUID]): The unique identifier for the maintenance request.
        title (Optional[str]): The title of the maintenance request.
        description (Optional[str]): The description of the maintenance request.
        status (Optional[MaintenanceStatusEnum]): The status of the maintenance request.
        priority (Optional[int]): The priority of the maintenance request.
        requested_by (Optional[Union[UUID, UserBase]]): The user who requested the maintenance.
        property_unit_assoc_id (Optional[Union[UUID, Any]]): The associated property unit.
        scheduled_date (Optional[datetime]): The scheduled date for the maintenance.
        completed_date (Optional[datetime]): The completed date for the maintenance.
        is_emergency (Optional[bool]): Indicates if the maintenance request is an emergency.
    """
    task_number: Optional[Annotated[str, constr(max_length=50)]] = None
    id: Optional[UUID] = None
    title: Optional[Annotated[str, constr(max_length=255)]] = None
    description: Optional[Annotated[str, constr(max_length=255)]] = None
    status: Optional[MaintenanceStatus] = None
    priority: Optional[int] = 0
    requested_by: Optional[Union[UUID, UserBase]] = None
    property_unit_assoc_id: Optional[Union[UUID, Any]] = None
    scheduled_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    is_emergency: Optional[bool] = False

    class Config:
        from_attributes = True
        use_enum_values = True
        populate_by_name = True


class MaintenanceRequestResponse(BaseModel):
    """
    Model for representing a maintenance request response.

    Attributes:
        id (Optional[UUID]): The unique identifier for the maintenance request.
        task_number (Optional[str]): The task number of the maintenance request.
        title (Optional[str]): The title of the maintenance request.
        description (Optional[str]): The description of the maintenance request.
        status (MaintenanceStatusEnum): The status of the maintenance request.
        priority (int): The priority of the maintenance request.
        requested_by (Optional[Union[UUID, UserBase]]): The user who requested the maintenance.
        property_unit_assoc (Optional[Union[UUID, Property, PropertyUnit, Any]]): The associated property unit.
        scheduled_date (Optional[datetime]): The scheduled date for the maintenance.
        completed_date (Optional[datetime]): The completed date for the maintenance.
        is_emergency (bool): Indicates if the maintenance request is an emergency.
        created_at (Optional[datetime]): The creation date of the maintenance request.
    """
    id: Optional[UUID] = None
    task_number: Optional[Annotated[str, constr(max_length=50)]] = None
    title: Optional[Annotated[str, constr(max_length=255)]] = None
    description: Optional[Annotated[str, constr(max_length=255)]] = None
    status: MaintenanceStatus
    priority: int = 0
    requested_by: Optional[Union[UUID, UserBase]] = None
    property_unit_assoc: Optional[Union[UUID, Property, PropertyUnit, Any]] = None
    scheduled_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    is_emergency: bool = False
    created_at: Optional[datetime] = None

    @classmethod
    def get_property_info(cls, property: Property) -> Property:
        """
        Get detailed property information.

        Args:
            property (Property): Property object.

        Returns:
            Property: Detailed property object.
        """
        return Property(
            property_unit_assoc_id=property.property_unit_assoc_id,
            name=property.name,
            property_type=property.property_type.name,
            amount=property.amount,
            security_deposit=property.security_deposit,
            commission=property.commission,
            floor_space=property.floor_space,
            num_units=property.num_units,
            num_bathrooms=property.num_bathrooms,
            num_garages=property.num_garages,
            has_balconies=property.has_balconies,
            has_parking_space=property.has_parking_space,
            pets_allowed=property.pets_allowed,
            description=property.description,
            property_status=property.property_status,
        )
    
    @classmethod
    def get_property_unit_info(cls, property_unit: PropertyUnit) -> PropertyUnit:
        """
        Get detailed property unit information.

        Args:
            property_unit (PropertyUnit): Property unit object.

        Returns:
            PropertyUnit: Detailed property unit object.
        """
        return PropertyUnit(
            property_unit_assoc_id=property_unit.property_unit_assoc_id,
            property_unit_code=property_unit.property_unit_code,
            property_unit_floor_space=property_unit.property_unit_floor_space,
            property_unit_amount=property_unit.property_unit_amount,
            property_floor_id=property_unit.property_floor_id,
            property_unit_notes=property_unit.property_unit_notes,
            has_amenities=property_unit.has_amenities,
            property_id=property_unit.property_id,
            property_unit_security_deposit=property_unit.property_unit_security_deposit,
            property_unit_commission=property_unit.property_unit_commission
        )
    
    @classmethod
    def get_property_unit_assoc(cls, property_unit_assoc: PropertyUnitAssoc) -> Union[Property, PropertyUnit, dict]:
        """
        Get detailed property unit association information.

        Args:
            property_unit_assoc (PropertyUnitAssoc): Property unit association object.

        Returns:
            Union[Property, PropertyUnit, dict]: Detailed property unit association object.
        """
        if property_unit_assoc is None:
            return {}
        
        if property_unit_assoc.property_unit_type == "Units":
            return cls.get_property_unit_info(property_unit_assoc)
        else:
            return cls.get_property_info(property_unit_assoc)

    @classmethod
    def from_orm_model(cls, maintenance_request: MaintenanceRequestModel) -> 'MaintenanceRequestResponse':
        """
        Create a MaintenanceRequestResponse instance from an ORM model.

        Args:
            maintenance_request (MaintenanceRequestModel): Maintenance request ORM model.

        Returns:
            MaintenanceRequestResponse: Maintenance request response object.
        """
        return cls(
            id=maintenance_request.id,
            task_number=maintenance_request.task_number,
            title=maintenance_request.title,
            description=maintenance_request.description,
            status=maintenance_request.status,
            priority=maintenance_request.priority,
            requested_by=maintenance_request.user,
            property_unit_assoc=cls.get_property_unit_assoc(maintenance_request.property_unit_assoc),
            scheduled_date=maintenance_request.scheduled_date,
            completed_date=maintenance_request.completed_date,
            is_emergency=maintenance_request.is_emergency,
            created_at=maintenance_request.created_at
        ).model_dump()
