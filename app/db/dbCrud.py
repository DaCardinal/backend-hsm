from typing import Type, TypeVar, Generic, Dict, Any
from sqlalchemy import and_
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


DBModelType = TypeVar("DBModelType")

class CreateMixin:
    model: Type[DBModelType]
    
    async def create(self, db_session: AsyncSession, obj_in) -> DBModelType:
        db_obj = self.model(**obj_in)
        db_session.add(db_obj)
        await db_session.commit()
        await db_session.refresh(db_obj)

        return db_obj
    
class ReadMixin:
    model: Type[DBModelType]

    async def get(self, db_session: AsyncSession, id: int) -> DBModelType:
        q = await db_session.execute(select(self.model).filter(self.model.id == id))

        return q.scalar_one_or_none()

    async def get_all(self, db_session: AsyncSession, skip=0, limit=100) -> list[DBModelType]:
        query = select(self.model).offset(skip).limit(limit)
        result = await db_session.execute(query)

        return result.scalars().all()
    
    async def query(self, db_session: AsyncSession, filters: Dict[str, Any], single=False, options=None) -> list[DBModelType]:
        conditions = [getattr(self.model, k) == v for k, v in filters.items()]
        query = select(self.model).filter(and_(*conditions))
        
        if options:
            query = query.options(*options)
        result = await db_session.execute(query)

        return result.scalar_one_or_none() if single else result.scalars().all()

class UpdateMixin:
    model: Type[DBModelType]

    async def update(self, db_session: AsyncSession, db_obj: DBModelType, obj_in: Dict[str, Any]) -> DBModelType:
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        db_session.add(db_obj)
        await db_session.commit()
        await db_session.refresh(db_obj)

        return db_obj

class DeleteMixin:
    model: Type[DBModelType]
    
    async def delete(self, db_session: AsyncSession, db_obj: DBModelType) -> DBModelType:
        await db_session.delete(db_obj)
        await db_session.commit()

class DBOperations(CreateMixin, ReadMixin, UpdateMixin, DeleteMixin):
    def __init__(self, model: Generic[DBModelType]):
        self.model = model