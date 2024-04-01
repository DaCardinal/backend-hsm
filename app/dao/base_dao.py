from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Type, TypeVar, Generic, List

DBModelType = TypeVar("DBModelType")

class AsyncCreateMixin(Generic[DBModelType]):
    model: Type[DBModelType]

    async def create(self, db_session: AsyncSession, *, obj_in) -> DBModelType:
        db_obj = self.model(**obj_in.dict())
        db_session.add(db_obj)
        await db_session.commit()
        await db_session.refresh(db_obj)
        return db_obj

class AsyncReadMixin(Generic[DBModelType]):
    model: Type[DBModelType]

    async def get(self, db_session: AsyncSession, item_id: int) -> DBModelType:
        result = await db_session.execute(select(self.model).filter(self.model.id == item_id))
        return result.scalars().first()

    async def get_all(self, db_session: AsyncSession, skip: int = 0, limit: int = 100) -> List[DBModelType]:
        result = await db_session.execute(select(self.model).offset(skip).limit(limit))
        return result.scalars().all()

    async def _query(self, db_session: AsyncSession, *args, **kwargs) -> List[DBModelType]:
        result = await db_session.execute(select(self.model).filter(*args, **kwargs))
        return result.scalars().all()

class AsyncUpdateMixin(Generic[DBModelType]):
    model: Type[DBModelType]

    async def update(self, db_session: AsyncSession, *, db_obj: DBModelType, obj_in) -> DBModelType:
        obj_data = obj_in.dict(exclude_unset=True)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        await db_session.commit()
        await db_session.refresh(db_obj)
        return db_obj

class AsyncDeleteMixin(Generic[DBModelType]):
    model: Type[DBModelType]

    async def delete(self, db_session: AsyncSession, *, item_id: int) -> DBModelType:
        obj = await db_session.get(self.model, item_id)
        await db_session.delete(obj)
        await db_session.commit()
        return obj

class BaseDAO(AsyncCreateMixin, AsyncReadMixin, AsyncUpdateMixin, AsyncDeleteMixin, Generic[DBModelType]):
    def __init__(self, model: Type[DBModelType]):
        self.model = model