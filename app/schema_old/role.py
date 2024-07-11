from uuid import UUID
from typing import List, Optional
from pydantic import BaseModel, Field

class Permission(BaseModel):
    permission_id: Optional[UUID] = Field(...)
    name: Optional[str] = Field(None, max_length=80)
    alias: Optional[str] = Field(None, max_length=80, unique=True)
    description: Optional[str] = None

    class Config:
        from_attributes = True

class RoleBase(BaseModel):
    name: str = Field(None, max_length=80)
    alias: Optional[str] = Field(None, max_length=80, unique=True)
    description: Optional[str] = None
    
    class Config:
        from_attributes = True

class RoleCreateSchema(RoleBase):
    
    class Config:
        from_attributes = True

class RoleUpdateSchema(RoleBase):
    
    class Config:
        from_attributes = True

class UserRoleInfo(BaseModel):
    alias: Optional[str]

    class Config: 
        __allow_unmapped__ = True
        from_attributes = True
        use_enum_values = True

class Role(BaseModel):
    role_id: UUID = Field(...)
    name: str = Field(None, max_length=80)
    alias: Optional[str] = Field(None, max_length=80, unique=True)
    description: Optional[str] = None
    permissions: Optional[List[Permission]]

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "role_id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Administrator",
                "alias": "admin",
                "description": "Has full access to all settings."
            }
        }