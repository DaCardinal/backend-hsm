from uuid import UUID
from datetime import datetime
from typing import Any, List, Optional, Annotated
from pydantic import BaseModel, constr, EmailStr

# schemas
from app.schema.user import UserBase, User

# models
from app.models import Message as MessageModel, MessageRecipient as MessageRecipientModel

class EmailBody(BaseModel):
    """
    Model for representing the body of an email.

    Attributes:
        to (EmailStr): The recipient's email address.
        subject (str): The subject of the email.
        message (str): The body of the email.
    """
    to: EmailStr
    subject: Annotated[str, constr(max_length=255)]
    message: Annotated[str, constr(max_length=2000)]

    class Config:
        from_attributes = True  

class MessageCreate(BaseModel):
    """
    Schema for creating a message.

    Attributes:
        subject (str): The subject of the message.
        message_body (str): The body of the message.
        sender_id (UUID): The unique identifier of the sender.
        is_draft (Optional[bool]): Indicates if the message is a draft.
        is_scheduled (Optional[bool]): Indicates if the message is scheduled.
        recipient_ids (Optional[List[UUID]]): List of recipient IDs.
        recipient_groups (Optional[List[UUID]]): List of recipient group IDs.
    """
    subject: Annotated[str, constr(max_length=255)]
    message_body: Annotated[str, constr(max_length=2000)]
    sender_id: UUID
    is_draft: Optional[bool] = False
    is_scheduled: Optional[bool] = False
    recipient_ids: Optional[List[UUID]] = None
    recipient_groups: Optional[List[UUID]] = None

    class Config:
        from_attributes = True  

class MessageReply(BaseModel):
    """
    Schema for replying to a message.

    Attributes:
        message_body (str): The body of the reply message.
        sender_id (UUID): The unique identifier of the sender.
        parent_message_id (UUID): The unique identifier of the parent message.
        recipient_ids (Optional[List[UUID]]): List of recipient IDs.
        recipient_groups (Optional[List[UUID]]): List of recipient group IDs.
    """
    message_body: Annotated[str, constr(max_length=2000)]
    sender_id: UUID
    parent_message_id: UUID
    recipient_ids: Optional[List[UUID]] = None
    recipient_groups: Optional[List[UUID]] = None

    class Config:
        from_attributes = True  

class MessageResponseModel(BaseModel):
    """
    Model for representing a message response.

    Attributes:
        message_id (Optional[UUID]): The unique identifier of the message.
        subject (Optional[str]): The subject of the message.
        sender (Optional[UserBase]): The sender of the message.
        recipients (Optional[List[UserBase]]): List of recipients of the message.
        message_body (Optional[str]): The body of the message.
        parent_message_id (Optional[UUID]): The unique identifier of the parent message.
        thread_id (Optional[UUID]): The unique identifier of the message thread.
        is_draft (Optional[bool]): Indicates if the message is a draft.
        is_notification (Optional[bool]): Indicates if the message is a notification.
        is_reminder (Optional[bool]): Indicates if the message is a reminder.
        is_scheduled (Optional[bool]): Indicates if the message is scheduled.
        is_read (Optional[bool]): Indicates if the message is read.
        date_created (Optional[datetime]): The date the message was created.
        scheduled_date (Optional[datetime]): The scheduled date for the message.
        next_remind_date (Optional[datetime]): The next reminder date for the message.
    """
    message_id: Optional[UUID] = None
    subject: Optional[Annotated[str, constr(max_length=255)]] = None
    sender: Optional[UserBase] = None
    recipients: Optional[List[UserBase]] = None
    message_body: Optional[Annotated[str, constr(max_length=2000)]] = None
    parent_message_id: Optional[UUID] = None
    thread_id: Optional[UUID] = None
    is_draft: Optional[bool] = False
    is_notification: Optional[bool] = False
    is_reminder: Optional[bool] = False
    is_scheduled: Optional[bool] = False
    is_read: Optional[bool] = False
    date_created: Optional[datetime] = None
    scheduled_date: Optional[datetime] = None
    next_remind_date: Optional[datetime] = None

    class Config:
        from_attributes = True  
        use_enum_values = True
        populate_by_name = True
        arbitrary_types_allowed = True

    @classmethod
    def get_user_info(cls, recipients: List[MessageRecipientModel]) -> List[UserBase]:
        """
        Get basic user information for recipients.

        Args:
            recipients (List[MessageRecipientModel]): List of message recipients.

        Returns:
            List[UserBase]: List of basic user information.
        """
        results = []
        for recipient in recipients:
            user : User = recipient.recipient

            results.append(UserBase(
                user_id=user.user_id,
                first_name=user.first_name,
                last_name=user.last_name,
                photo_url=user.photo_url,
                email=user.email,
                gender=user.gender,
                identification_number=user.identification_number,
                phone_number=user.phone_number
            ))
        return results

    @classmethod
    def get_message_group_info(cls, recipients: List[MessageRecipientModel]) -> List[Any]:
        """
        Get group information for recipients.

        Args:
            recipients (List[MessageRecipient]): List of message recipients.

        Returns:
            List[Any]: List of group information.
        """
        results = []
        
        for recipient in recipients:
            results.append(recipient)

        return results
    
    @classmethod
    def from_orm_model(cls, message: MessageModel) -> 'MessageResponseModel':
        """
        Create a MessageResponseModel instance from an ORM model.

        Args:
            message (MessageModel): Message ORM model.

        Returns:
            MessageResponseModel: Message response object.
        """
        return cls(
            message_id=message.message_id,
            message_body=message.message_body,
            subject=message.subject,
            sender=message.sender,
            parent_message_id=message.parent_message_id,
            thread_id=message.thread_id,
            is_draft=message.is_draft,
            is_notification=message.is_notification,
            is_reminder=message.is_reminder,
            is_scheduled=message.is_scheduled,
            is_read=message.is_read,
            date_created=message.date_created,
            scheduled_date=message.scheduled_date,
            next_remind_date=message.next_remind_date,
            recipients=cls.get_user_info(message.recipients)
        ).model_dump()