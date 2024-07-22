from uuid import UUID
from pydantic import BaseModel, ConfigDict, constr
from typing import Optional, Annotated


class Permission(BaseModel):
    """
    Model for representing a permission.

    Attributes:
        permission_id (UUID): The unique identifier for the permission.
        name (Optional[str]): The name of the permission, with a maximum length of 80 characters.
        alias (Optional[str]): An optional alias for the permission, with a maximum length of 80 characters.
        description (Optional[str]): An optional description of the permission.
    """

    permission_id: UUID
    name: Optional[Annotated[str, constr(max_length=80)]] = None
    alias: Optional[Annotated[str, constr(max_length=80)]] = None
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
