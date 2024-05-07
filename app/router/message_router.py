from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4, UUID
from typing import List
from fastapi import HTTPException, Depends
from sqlalchemy.orm import aliased
from sqlalchemy import or_, select

from app.models import Message, MessageRecipient, PropertyUnitAssoc, UnderContract
from app.dao.message_dao import MessageDAO
from app.utils.response import DAOResponse
from app.schema import MessageSchema, MessageCreate, MessageReply, MessageResponseModel
from app.router.base_router import BaseCRUDRouter

class MessageRouter(BaseCRUDRouter):

    def __init__(self, dao: MessageDAO = MessageDAO(Message), prefix: str = "", tags: List[str] = []):
        
        MessageSchema["create_schema"] = MessageCreate
        super().__init__(dao=dao, schemas=MessageSchema, prefix=prefix,tags = tags)
        self.dao = dao
        self.register_routes()

    def register_routes(self):
        @self.router.post("/reply/")
        async def reply_to_message(message: MessageReply, db: AsyncSession = Depends(self.get_db)):
            parent_message : Message = await self.dao.query(db_session=db, filters={"message_id":  message.parent_message_id}, single=True)
            
            if not parent_message:
                raise HTTPException(status_code=404, detail="Parent message not found")
            
            return await self.dao.create(db_session=db, obj_in=Message(
                message_id=uuid4(),
                subject=parent_message.subject,
                message_body=message.message_body,
                sender_id=message.sender_id,
                parent_message_id=message.parent_message_id,
                thread_id=parent_message.thread_id
            ))
        
        @self.router.get("/users/{user_id}/outbox", response_model=DAOResponse[List[MessageResponseModel]])
        async def get_user_outbox(user_id: UUID, db: AsyncSession = Depends(self.get_db)):
            # outbox_messages = db.query(Message).filter(Message.sender_id == user_id).order_by(Message.date_created.desc()).all()
            outbox_messages = await self.dao.query(db_session=db, filters={"sender_id":  user_id})
            
            return DAOResponse[List[MessageResponseModel]](success=True, data=[{
                "message_id": message.message_id,
                "subject": message.subject,
                "sender_id": message.sender_id,
                "body": message.message_body,
                "date_created": message.date_created.isoformat()
            } for message in outbox_messages])

        @self.router.get("/users/{user_id}/inbox", response_model=DAOResponse[List[MessageResponseModel]])
        async def get_user_inbox(user_id: UUID, db: AsyncSession = Depends(self.get_db)):
            # Alias for clarity when querying
            group_alias = aliased(PropertyUnitAssoc)

            # Asynchronously fetch the user's groups
            user_groups_stmt = select(group_alias.property_unit_assoc_id).\
                join(UnderContract, group_alias.property_unit_assoc_id == UnderContract.property_unit_assoc_id).\
                where(UnderContract.client_id == user_id)
            result = await db.execute(user_groups_stmt)
            user_groups_ids = [group.property_unit_assoc_id for group in result.scalars().all()]

            # Construct a list of group IDs for use in the next query
            if not user_groups_ids:
                user_groups_ids = []  # Ensure it's a list even if empty

            # Asynchronously fetch inbox messages
            inbox_stmt = select(Message).\
                join(MessageRecipient, Message.message_id == MessageRecipient.message_id).\
                where(
                    or_(
                        MessageRecipient.recipient_id == user_id,
                        MessageRecipient.recipient_group_id.in_(user_groups_ids) if user_groups_ids else False
                    )
                ).order_by(Message.date_created.desc())
            result = await db.execute(inbox_stmt)
            inbox_messages = result.scalars().all()
        
            return DAOResponse[List[MessageResponseModel]](success=True, data=[{
                "message_id": message.message_id,
                "subject": message.subject,
                "sender_id": message.sender_id,
                "body": message.message_body,
                "date_created": message.date_created.isoformat()
            } for message in inbox_messages])