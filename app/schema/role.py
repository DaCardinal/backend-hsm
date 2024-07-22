from uuid import UUID
from pydantic import BaseModel, ConfigDict, constr
from typing import List, Optional, Annotated

from app.schema.permission import Permission
from app.models.role import Role as RoleModel


class RoleBase(BaseModel):
    name: Optional[Annotated[str, constr(max_length=80)]] = None
    alias: Optional[Annotated[str, constr(max_length=80)]] = None
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class Role(BaseModel):
    role_id: UUID
    name: Optional[Annotated[str, constr(max_length=80)]] = None
    alias: Optional[Annotated[str, constr(max_length=80)]] = None
    description: Optional[str] = None
    permissions: Optional[List[Permission]] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "role_id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Administrator",
                "alias": "admin",
                "description": "Has full access to all settings.",
            }
        },
    )


class RoleCreateSchema(RoleBase):
    model_config = ConfigDict(from_attributes=True)


class RoleUpdateSchema(RoleBase):
    model_config = ConfigDict(from_attributes=True)


class UserRoleInfo(BaseModel):
    alias: Optional[str]

    model_config = ConfigDict(
        __allow_unmapped__=True, from_attributes=True, use_enum_values=True
    )


class RoleResponse(BaseModel):
    role_id: UUID
    name: Optional[Annotated[str, constr(max_length=80)]] = None
    alias: Optional[Annotated[str, constr(max_length=80)]] = None
    description: Optional[str] = None
    # permissions: Optional[List[Permission]] = None

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm_model(cls, role: RoleModel):
        """
        Create a RoleResponse instance from an ORM model.

        Args:
            role (RoleModel): Role ORM model.

        Returns:
            RoleResponse: Role response object.
        """
        return cls(
            role_id=role.role_id,
            name=role.name,
            alias=role.alias,
            description=role.description,
            # permissions = role.permissions,
        ).model_dump()
