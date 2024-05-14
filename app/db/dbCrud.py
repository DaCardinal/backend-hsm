from typing import List, Type, TypeVar, Generic, Dict, Any, Union, Optional
from uuid import UUID
from pydantic import BaseModel, create_model
from sqlalchemy import and_
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import inspect
from sqlalchemy.orm import selectinload

from app.utils.response import DAOResponse

DBModelType = TypeVar("DBModelType")

class UtilsMixin:
    async def commit_and_refresh(self, db_session: AsyncSession, obj: DBModelType):
        try:
            await db_session.commit()
            await db_session.refresh(obj)
            return obj
        except Exception as e:
            db_session.rollback()
            return DAOResponse(success=False, error=f"Error committing data: {str(e)}")
        
class CreateMixin(UtilsMixin):
    model: Type[DBModelType]
    
    async def create(self, db_session: AsyncSession, obj_in) -> DBModelType:
        db_obj = self.model(**obj_in)
        db_session.add(db_obj)

        return await self.commit_and_refresh(db_session=db_session, obj=db_obj)
    
class ReadMixin(UtilsMixin):
    model: Type[DBModelType]
    load_parent_relationships: bool

    async def get(self, db_session: AsyncSession, id: Union[UUID | Any | int], skip=0, limit=100) -> DBModelType:
        # find primary key
        primary_keys = [(key.name, key) for key in inspect(self.model).primary_key]
        primary_key = primary_keys[0]
        
        mapper = inspect(self.model)
        relationships = [relationship.key for relationship in mapper.relationships]
        query_options = [selectinload(getattr(self.model, attr)) for attr in relationships] if self.load_parent_relationships else []

        query = select(self.model).filter(primary_key[1] == id).options(*query_options).offset(skip).limit(limit)
        executed_query = await db_session.execute(query)
        result = executed_query.scalar_one_or_none()

        return result

    async def get_all(self, db_session: AsyncSession, skip=0, limit=100) -> list[DBModelType]:

        # Dynamically access the relationship attribute using getattr
        mapper = inspect(self.model)
        relationships = [relationship.key for relationship in mapper.relationships]
        query_options = [selectinload(getattr(self.model, attr)) for attr in relationships] if self.load_parent_relationships else []

        query = select(self.model).options(*query_options).offset(skip).limit(limit)
        executed_query = await db_session.execute(query)
        result = executed_query.scalars().all()
        
        return result
    
    async def query(self, db_session: AsyncSession, filters: Dict[str, Any], single=False, options=None) -> list[DBModelType]:
        conditions = [getattr(self.model, k) == v for k, v in filters.items()]
        query = select(self.model).filter(and_(*conditions))
        
        if options:
            query = query.options(*options)
        query_result = await db_session.execute(query)

        return query_result.scalar_one_or_none() if single else query_result.scalars().all()

    async def query_on_create(self, db_session: AsyncSession, filters: Dict[str, Any], single=False, options=None, create_if_not_exist = False):
        result = await self.query(db_session=db_session, filters=filters, single=single, options=options)

        if result:
            return result
        elif create_if_not_exist:
            db_obj = self.model(**filters)
            db_session.add(db_obj)

            return await self.commit_and_refresh(db_session=db_session, obj=db_obj)
        
class UpdateMixin(UtilsMixin):
    model: Type[DBModelType]

    async def update(self, db_session: AsyncSession, db_obj: DBModelType, obj_in: Dict[str, Any]) -> DBModelType:
        for field, value in obj_in:
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        db_session.add(db_obj)
        
        return await self.commit_and_refresh(db_session=db_session, obj=db_obj)

class DeleteMixin(UtilsMixin):
    model: Type[DBModelType]
    
    async def delete(self, db_session: AsyncSession, db_obj: DBModelType) -> DBModelType:
        await db_session.delete(db_obj)
        await db_session.commit()
        
class DBOperations(CreateMixin, ReadMixin, UpdateMixin, DeleteMixin):
    def __init__(self, model: Generic[DBModelType], load_parent_relationships: bool = False, load_child_relationships: bool = False, excludes = []):
        self.model = model
        self.load_parent_relationships = load_parent_relationships
        self.load_child_relationships = load_child_relationships
        self.excludes = excludes