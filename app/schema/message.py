from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import datetime


class MessageCreate(BaseModel):
    subject: str
    message_body: str
    sender_id: UUID
    is_draft: Optional[bool] = False
    recipient_ids: Optional[List[UUID]]
    recipient_groups: Optional[List[UUID]]

    class Config:
        from_attributes = True

class MessageReply(BaseModel):
    message_body: str
    sender_id: UUID
    parent_message_id: UUID
    recipient_ids: Optional[List[UUID]]
    recipient_groups: Optional[List[UUID]]

    class Config:
        from_attributes = True

class MessageResponseModel(BaseModel):
    message_id: UUID
    subject: str
    thread_id: Optional[UUID]
    sender_id: UUID
    body: str
    date_created: datetime

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    email: str

    class Config:
        from_attributes = True

class PropertyUnitAssocCreate(BaseModel):
    property_name: str
    location: str

    class Config:
        from_attributes = True

class PropertyUnitAssocResponse(BaseModel):
    property_unit_assoc_id: UUID
    property_name: str
    location: str

    class Config:
        from_attributes = True

class UserGroupAddition(BaseModel):
    user_id: UUID
    property_unit_assoc_id: UUID

    class Config:
        from_attributes = True
