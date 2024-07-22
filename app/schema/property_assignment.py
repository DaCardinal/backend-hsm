from enum import Enum
from uuid import UUID
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

from app.schema.mixins.user_mixins import UserBase


class AssignmentType(str, Enum):
    """
    Enum representing types of assignments.
    """

    other = "other"
    handler = "handler"
    landlord = "landlord"
    contractor = "contractor"


class PropertyAssignmentBase(BaseModel):
    """
    Base schema for PropertyAssignment model, containing common attributes.

    Attributes:
        property_unit_assoc_id (UUID): The UUID of the associated property unit.
        user_id (UUID): The UUID of the user assigned to the property.
        assignment_type (AssignmentType): The type of assignment.
        date_from (datetime): The start date of the assignment.
        date_to (Optional[datetime]): The optional end date of the assignment.
        notes (Optional[str]): Additional notes about the assignment.
    """

    property_unit_assoc_id: UUID
    user_id: Optional[UserBase]
    assignment_type: AssignmentType
    date_from: datetime
    date_to: Optional[datetime] = None
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class PropertyAssignment(BaseModel):
    """
    Base schema for PropertyAssignment model, containing common attributes.

    Attributes:
        property_assignment_id (UUID): The unique identifier for the property assignment.
        property_unit_assoc_id (UUID): The UUID of the associated property unit.
        user_id (UUID): The UUID of the user assigned to the property.
        assignment_type (AssignmentType): The type of assignment.
        date_from (datetime): The start date of the assignment.
        date_to (Optional[datetime]): The optional end date of the assignment.
        notes (Optional[str]): Additional notes about the assignment.
    """

    property_assignment_id: UUID
    property_unit_assoc_id: UUID
    user_id: Optional[UserBase]
    assignment_type: AssignmentType
    date_from: datetime
    date_to: Optional[datetime] = None
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class PropertyAssignmentCreate(BaseModel):
    """
    Schema for creating a new PropertyAssignment.

    Attributes:
        property_unit_assoc_id (UUID): The UUID of the associated property unit.
        user_id (UUID): The UUID of the user assigned to the property.
        assignment_type (AssignmentType): The type of assignment.
        date_from (datetime): The start date of the assignment.
        date_to (Optional[datetime]): The optional end date of the assignment.
        notes (Optional[str]): Additional notes about the assignment.
    """

    property_unit_assoc_id: UUID
    user_id: UUID
    assignment_type: AssignmentType
    date_from: datetime
    date_to: Optional[datetime] = None
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class PropertyAssignmentUpdate(BaseModel):
    """
    Schema for updating an existing PropertyAssignment.

    Attributes:
        property_assignment_id (UUID): The unique identifier for the property assignment.
        property_unit_assoc_id (UUID): The UUID of the associated property unit.
        user_id (UUID): The UUID of the user assigned to the property.
        assignment_type (AssignmentType): The type of assignment.
        date_from (datetime): The start date of the assignment.
        date_to (Optional[datetime]): The optional end date of the assignment.
        notes (Optional[str]): Additional notes about the assignment.
    """

    property_assignment_id: UUID
    property_unit_assoc_id: UUID
    user_id: UUID
    assignment_type: AssignmentType
    date_from: datetime
    date_to: Optional[datetime] = None
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
