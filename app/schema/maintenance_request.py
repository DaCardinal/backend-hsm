from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict, constr
from typing import Any, Optional, Union, Annotated

# schemas
from app.schema.user import UserBase
from app.schema.enums import MaintenanceStatus

# mixins
from app.schema.mixins.property_mixin import (
    Property,
    PropertyUnit,
    PropertyDetailsMixin,
)

# models
from app.models.maintenance_request import MaintenanceRequest as MaintenanceRequestModel


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

    model_config = ConfigDict(from_attributes=True)


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

    model_config = ConfigDict(from_attributes=True)


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

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        use_enum_values=True,
    )


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

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        use_enum_values=True,
    )


class MaintenanceRequestResponse(BaseModel, PropertyDetailsMixin):
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
    def from_orm_model(
        cls, maintenance_request: MaintenanceRequestModel
    ) -> "MaintenanceRequestResponse":
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
            property_unit_assoc=cls.get_property_details(
                maintenance_request.property_unit_assoc
            ),
            scheduled_date=maintenance_request.scheduled_date,
            completed_date=maintenance_request.completed_date,
            is_emergency=maintenance_request.is_emergency,
            created_at=maintenance_request.created_at,
        ).model_dump()
