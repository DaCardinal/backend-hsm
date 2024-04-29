from uuid import UUID
from pydantic import ValidationError, BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import selectinload
from typing import Any, Dict, List, Type, Optional, Union, override

from app.dao.base_dao import BaseDAO
from app.models import Property
from app.utils.response import DAOResponse

class PropertyDAO(BaseDAO[Property]):
    def __init__(self, model: Type[Property]):
        super().__init__(model)

    @override
    async def create(self, db_session: AsyncSession, obj_in: Union[Property | Dict]) -> DAOResponse:
        print("here now")
        pass