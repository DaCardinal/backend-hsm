from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from app.models import Message as MessageModel, User as UserModel, MessageRecipient
from app.schema import UserBase

class EmailBody(BaseModel):
    to: str
    subject: str
    message: str

    class Config:
        from_attributes = True
    
class MessageCreate(BaseModel):
    subject: str
    message_body: str
    sender_id: UUID
    is_draft: Optional[bool] = False
    is_scheduled: Optional[bool] = False
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
    message_id: Optional[UUID]
    subject: Optional[str]
    sender: Optional[UserBase]
    recipients: Optional[List[UserBase]]
    message_body: Optional[str]
    parent_message_id: Optional[UUID]
    thread_id: Optional[UUID]
    is_draft: Optional[bool] = False
    is_notification: Optional[bool] = False
    is_reminder: Optional[bool] = False
    is_scheduled: Optional[bool] = False
    is_read: Optional[bool] = False
    date_created:  Optional[datetime]
    scheduled_date:  Optional[datetime]
    next_remind_date: Optional[datetime]

    class Config:
        from_attributes = True
        use_enum_values = True
        populate_by_name = True
        arbitrary_types_allowed=True

    @classmethod
    def get_user_info(cls, recipients: MessageRecipient):
        recipients : List[MessageRecipient] = recipients
        results = []

        for recipient in recipients:
            recipient : MessageRecipient = recipient
            user : UserBase = recipient.recipient

            results.append(UserModel(
                user_id = user.user_id,
                first_name=user.first_name,
                last_name=user.last_name,
                photo_url=user.photo_url,
                email=user.email,
                gender=user.gender,
                identification_number= user.identification_number,
                phone_number = user.phone_number
            ))
        return results

    @classmethod
    def get_message_group_info(cls, recipients: MessageRecipient):
        recipients : List[MessageRecipient] = recipients
        results = []

        for recipient in recipients:
            recipient : MessageRecipient = recipient

        return results
    
    @classmethod
    def from_orm_model(cls, message: MessageModel):
        
        result = cls(
            message_id = message.message_id,
            message_body = message.message_body,
            subject = message.subject,
            sender = message.sender,
            parent_message_id = message.parent_message_id,
            thread_id = message.thread_id,
            is_draft = message.is_draft,
            is_notification = message.is_notification,
            is_reminder = message.is_reminder,
            is_scheduled = message.is_scheduled,
            is_read = message.is_read,
            date_created = message.date_created,
            scheduled_date = message.scheduled_date,
            next_remind_date = message.next_remind_date,
            recipients = cls.get_user_info(message.recipients)
        ).model_dump()

        return result

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
