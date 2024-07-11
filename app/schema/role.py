from uuid import UUID
from pydantic import BaseModel, constr
from typing import List, Optional, Annotated

from app.schema.permission import Permission

class RoleBase(BaseModel):
    name: Optional[Annotated[str, constr(max_length=80)]] = None
    alias: Optional[Annotated[str, constr(max_length=80)]] = None
    description: Optional[str] = None
    
    class Config:
        from_attributes = True

class Role(BaseModel):
    role_id: UUID
    name: Optional[Annotated[str, constr(max_length=80)]] = None
    alias: Optional[Annotated[str, constr(max_length=80)]] = None
    description: Optional[str] = None
    permissions: Optional[List[Permission]] = None
    
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