from typing import TypeVar, Generic, Dict, Any
from sqlalchemy import and_
from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


DBModelType = TypeVar("DBModelType")

class CreateMixin:
    async def create(self, db_session: AsyncSession, obj_in) -> DBModelType:
        async with db_session as db:
            db_obj = self.model(**obj_in)
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
        return db_obj
    
class ReadMixin:
    async def get(self, db_session: AsyncSession, id: int) -> DBModelType:
        async with db_session as db:
            q = await db.execute(select(self.model).filter(self.model.id == id))
            try:
                return q.scalar_one()
            except NoResultFound:
                return None

    async def get_all(self, db_session: AsyncSession, skip=0, limit=100) -> list[DBModelType]:
        async with db_session as db:
            q = await db.execute(select(self.model).offset(skip).limit(limit))
        return q.scalars().all()

    async def get_single(db_session: AsyncSession, user_id: int) -> DBModelType:
        user = (await db_session.scalars(select(DBModelType).where(DBModelType.id == user_id))).first()
        if not user:
            raise NoResultFound
        return user
    
    async def query(self, db_session: AsyncSession, filters: Dict[str, Any], single=False, options=None) -> list[DBModelType]:
        async with db_session as db:
            conditions = [getattr(self.model, k) == v for k, v in filters.items()]
            query = select(self.model).filter(and_(*conditions))
            
            # Apply options if provided
            if options:
                for option in options:
                    query = query.options(option)
            
            result = await db.execute(query)
            
            return result.scalar_one_or_none() if single else result.scalars().all()
        
    async def query2(self, db_session: AsyncSession, filters: Dict[str, Any], single = False) -> list[DBModelType]:
        async with db_session as db:
            conditions = [getattr(self.model, k) == v for k, v in filters.items()]
            query = select(self.model).filter(and_(*conditions))
            result = await db.execute(query)
            
        return result.scalar_one_or_none() if single else result.scalars().all()

class UpdateMixin:
    async def update(self, db_session: AsyncSession, db_obj: DBModelType, obj_in) -> DBModelType:
        async with db_session as db:
            obj_data = db_obj.__dict__
            update_data = obj_in.dict(exclude_unset=True)

            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])

            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
        return db_obj

class DeleteMixin:
    async def delete(self, db_session: AsyncSession, db_obj: DBModelType) -> DBModelType:
        async with db_session as db:
            await db.delete(db_obj)
            await db.commit()
        return db_obj

class DBOperations(CreateMixin, ReadMixin, UpdateMixin, DeleteMixin):
    def __init__(self, model: Generic[DBModelType]):
        self.model = model