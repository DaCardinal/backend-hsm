from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing_extensions import override

from app.dao.base_dao import BaseDAO
from app.utils.response import DAOResponse
from app.schema import MessageCreate, MessageResponseModel, MessageReply
from app.models import Message, MessageRecipient

class MessageDAO(BaseDAO[Message]):
    def __init__(self, model: Type[Message]):
        super().__init__(model)
        self.primary_key = "message_id"

    @override
    async def create(self, db_session: AsyncSession, obj_in: MessageCreate) -> DAOResponse[MessageResponseModel]:
        try:
            obj_in: dict = obj_in
            message_items = {key: value for key, value in obj_in.items() if key not in ['recipient_ids', 'recipient_groups']}
            
            # extract base information
            message_info = self.extract_model_data(message_items, MessageCreate)

            # create new user
            new_message: Message = await super().create(db_session=db_session, obj_in=message_info)
            new_message.thread_id = new_message.message_id
            new_message.parent_message_id = new_message.message_id

            # Create and add message recipients
            recipients = [MessageRecipient(recipient_id=rid, message_id=new_message.message_id, is_read=False) for rid in obj_in['recipient_ids']]
            recipients_groups = [MessageRecipient(recipient_group_id=rid, message_id=new_message.message_id, is_read=False) for rid in obj_in['recipient_groups']]
            db_session.add_all(recipients + recipients_groups)

            # commit transactions.
            for obj in recipients + recipients_groups:
                await self.commit_and_refresh(db_session=db_session, obj=obj)
                
            return DAOResponse[MessageResponseModel](success=True, data={
                "message_id": new_message.message_id,
                "sender_id": new_message.sender_id,
                "subject": new_message.subject,
                "body": new_message.message_body,
                "date_created": new_message.date_created.isoformat()
            })
        except NoResultFound:
            pass
        except Exception as e:
            await db_session.rollback()
            print(f"Fatal {str(e)}")

    async def reply_to_message(self, db_session: AsyncSession, message: MessageReply) -> DAOResponse[MessageResponseModel]:
        parent_message : Message = await self.query(db_session=db_session, filters={"message_id":  message.parent_message_id}, single=True)

        if not parent_message:
            raise NoResultFound(detail="Parent message not found")

        return await self.create(db_session=db_session, obj_in=Message(
            message_id=uuid4(),
            subject=parent_message.subject,
            message_body=message.message_body,
            sender_id=message.sender_id,
            parent_message_id=message.parent_message_id,
            thread_id=parent_message.thread_id
        ))