from uuid import UUID
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Type, TypeVar, Generic, Union

from app.db.dbCrud import DBOperations

DBModelType = TypeVar("DBModelType")

class BaseDAO(DBOperations, Generic[DBModelType]):
    def __init__(self, model: Type[DBModelType], load_parent_relationships: bool = False, load_child_relationships: bool = False, excludes = []):
        self.model = model
        self.load_parent_relationships = load_parent_relationships
        self.load_child_relationships = load_child_relationships
        self.excludes = excludes

    def decompose_dict(self, d):
        def is_class_instance_with_to_dict(val):
            return hasattr(val, 'to_dict') and callable(getattr(val, 'to_dict'))

        if isinstance(d, dict):
            decomposed = {}
            for key, value in d.items():
                if is_class_instance_with_to_dict(value):
                    decomposed[key] = value.to_dict()
                elif isinstance(value, dict):
                    decomposed[key] = self.decompose_dict(value)
                elif isinstance(value, list):
                    decomposed[key] = [self.decompose_dict(item.to_dict()) for item in value]
                else:
                    decomposed[key] = value
            return decomposed
        elif isinstance(d, list):
            return [self.decompose_dict(item) for item in d]
        else:
            return d
        
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

        if data is None:
            return None
        
        if isinstance(data, list):
            return [{key: data_item[key] for key in data_item if key in schema.model_fields} for data_item in data]
        
        return {key: data[key] for key in data if key in schema.model_fields}