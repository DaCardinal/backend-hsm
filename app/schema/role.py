from uuid import UUID
from typing import Optional
from pydantic import BaseModel, Field

class Role(BaseModel):
    role_id: UUID = Field(...)
    name: str = Field(None, max_length=80)
    alias: Optional[str] = Field(None, max_length=80, unique=True)
    description: Optional[str] = None

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