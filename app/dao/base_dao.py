from typing import Optional, Type, TypeVar, Generic

from pydantic import BaseModel

from app.db.dbCrud import DBOperations

DBModelType = TypeVar("DBModelType")

class BaseDAO(DBOperations, Generic[DBModelType]):
    def __init__(self, model: Type[DBModelType]):
        self.model = model

    def extract_model_data(self, data: dict, schema: Type[BaseModel], nested_key: Optional[str] = None) -> dict:
        if nested_key:
            data = data.get(nested_key, {})
        
        return {key: data[key] for key in data if key in schema.model_fields} if data else None