from sqlalchemy.orm import Session
from typing import Type, TypeVar, Generic, List

DBModelType = TypeVar("DBModelType")

class CreateMixin(Generic[DBModelType]):
    model: Type[DBModelType]

    def create(self, db_session: Session, *, obj_in) -> DBModelType:
        db_obj = self.model(**obj_in.dict())
        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj

class ReadMixin(Generic[DBModelType]):
    model: Type[DBModelType]

    def get(self, db_session: Session, item_id: int) -> DBModelType:
        return db_session.query(self.model).filter(self.model.id == item_id).first()

    def get_all(self, db_session: Session, skip: int = 0, limit: int = 100) -> List[DBModelType]:
        return db_session.query(self.model).offset(skip).limit(limit).all()
    
    def _query(self, db_session: Session, *args, **kwargs) -> List[DBModelType]:
        return db_session.query(self.model).filter(*args, **kwargs)

class UpdateMixin(Generic[DBModelType]):
    model: Type[DBModelType]

    def update(self, db_session: Session, *, db_obj: DBModelType, obj_in) -> DBModelType:
        obj_data = obj_in.dict(exclude_unset=True)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj

class DeleteMixin(Generic[DBModelType]):
    model: Type[DBModelType]

    def delete(self, db_session: Session, *, item_id: int) -> DBModelType:
        obj = db_session.query(self.model).get(item_id)
        db_session.delete(obj)
        db_session.commit()
        return obj

class BaseDAODeprecated(CreateMixin, ReadMixin, UpdateMixin, DeleteMixin, Generic[DBModelType]):
    def __init__(self, model: Type[DBModelType]):
        self.model = model