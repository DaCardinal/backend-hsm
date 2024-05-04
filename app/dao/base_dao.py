from typing import List, Optional, Type, TypeVar, Generic, Union
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.db.dbCrud import DBOperations

DBModelType = TypeVar("DBModelType")

class BaseDAO(DBOperations, Generic[DBModelType]):
    def __init__(self, model: Type[DBModelType]):
        self.model = model

    async def process_entity_details(self, db_session: AsyncSession, entity_id: UUID, entity_data: BaseModel, details_methods: dict):
        results = {}

        for detail_key, (method, schema) in details_methods.items():
            detail_data = self.extract_model_data(entity_data, schema, nested_key=detail_key)
            if detail_data:
                if isinstance(detail_data, list):
                    for entity_item in detail_data:
                        results[detail_key] = await method(db_session, entity_id, schema(**entity_item))
                else:
                    results[detail_key] = await method(db_session, entity_id, schema(**detail_data))
        
        return results
    
    def extract_model_data(self, data: dict, schema: Type[BaseModel], nested_key: Optional[str] = None) -> Union[List[dict] | dict]:
        data = data.get(nested_key, {}) if nested_key else data

        # check if data key is null
        if data is None:
            return None
        
        if isinstance(data, list):
            return [{key: data_item[key] for key in data_item if key in schema.model_fields} for data_item in data]
        
        return {key: data[key] for key in data if key in schema.model_fields}