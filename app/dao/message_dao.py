from uuid import UUID
from typing import Any, List, Type, Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound
from typing_extensions import override

from app.dao.base_dao import BaseDAO
from app.utils.settings import settings
from app.utils.response import DAOResponse
from app.models import Message, MessageRecipient
from app.schema import MessageCreate, MessageResponseModel

EMAIL = settings.EMAIL
EMAIL_PASSWORD = settings.EMAIL_PASSWORD
SERVER = settings.EMAIL_SERVER

class MessageDAO(BaseDAO[Message]):
    def __init__(self, model: Type[Message], load_parent_relationships: bool = False, load_child_relationships: bool = False):
        super().__init__(model, load_parent_relationships, load_child_relationships)
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

            await self.commit_and_refresh(db_session=db_session, obj=new_message)
            return DAOResponse[MessageResponseModel](success=True, data=MessageResponseModel.from_orm_model(new_message))
        except NoResultFound:
            return DAOResponse(success=False, error=f"MessageDAO Create Failure: {str(e)}")
        except Exception as e:
            await db_session.rollback()
            return DAOResponse(success=False, error=f"MessageDAO Create Failure: {str(e)}")

    @override
    async def get_all(self, db_session: AsyncSession, offset=0, limit=100) -> DAOResponse[List[MessageResponseModel]]:
        result = await super().get_all(db_session=db_session, offset=offset, limit=limit)
        
        # check if no result
        if not result:
            return DAOResponse(success=True, data=[])

        return DAOResponse[List[MessageResponseModel]](success=True, data=[MessageResponseModel.from_orm_model(r) for r in result])
    
    @override
    async def get(self, db_session: AsyncSession, id: Union[UUID | Any | int]) -> DAOResponse[MessageResponseModel]:
        result : Message = await super().get(db_session=db_session, id=id)

        # check if no result
        if not result:
            return DAOResponse(success=True, data={})

        return DAOResponse[MessageResponseModel](success=True, data=MessageResponseModel.from_orm_model(result))