from typing import Type, TypeVar, Generic

from app.db.dbCrud import DBOperations

DBModelType = TypeVar("DBModelType")

class BaseDAO(DBOperations, Generic[DBModelType]):
    def __init__(self, model: Type[DBModelType]):
        self.model = model