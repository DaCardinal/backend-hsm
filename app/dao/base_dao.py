from uuid import UUID
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Type, TypeVar, Generic, Union

from app.utils import DAOResponse
from app.db.dbCrud import DBOperations

DBModelType = TypeVar("DBModelType")

class BaseDAO(DBOperations, Generic[DBModelType]):
    # nesting type
    IMMEDIATE_CHILD = "immediate_child"
    NESTED_CHILD = "nested_child"
    NO_NESTED_CHILD = "parents_only"

    def __init__(self, model: Type[DBModelType], excludes = [], nesting_degree: str = NO_NESTED_CHILD):
        self.model = model
        self.nesting_degree = nesting_degree

        if self.nesting_degree == self.IMMEDIATE_CHILD:
            self.load_parent_relationships = True
            self.load_child_relationships = False
        elif self.nesting_degree == self.NESTED_CHILD:
            self.load_parent_relationships = True
            self.load_child_relationships = True
        elif self.nesting_degree == self.NO_NESTED_CHILD:
            self.load_parent_relationships = False
            self.load_child_relationships = False

        self.excludes = excludes

    def determine_schema(entity_data, key, full_schema, base_schema, id_key='id'):
        """
        Determines the appropriate schema class based on the provided entity data.

        :param entity_data: The data dictionary to check for the schema key.
        :param key: The key to look for in the entity_data dictionary.
        :param full_schema: The full schema class to return if the conditions are met.
        :param base_schema: The base schema class to return if the conditions are not met.
        :param id_key: The key to check for existence in the entity data's key.
        :return: The appropriate schema class.
        """
        if key in entity_data and entity_data[key]:
            # Check if id_key exists directly or in the first item of the list if the value is a list
            if id_key in entity_data[key] or (isinstance(entity_data[key], list) and id_key in entity_data[key][0]):
                return full_schema
        return base_schema

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
        
    def validate_errors(self, results):
        for result in results:
            result_value = results[result]
            
            if isinstance(result_value, DAOResponse) and result_value.success == False:
                raise Exception(str(result_value.error))
            
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
        
        # TODO: Add exception handler here for failed exceptions
        self.validate_errors(results)
        
        return results
    
    def extract_model_data(self, data: dict, schema: Type[BaseModel], nested_key: Optional[str] = None) -> Union[List[dict] | dict]:
        data = data.get(nested_key, {}) if nested_key else data

        if data is None:
            return None
        
        if isinstance(data, list):
            return [{key: data_item[key] for key in data_item if key in schema.model_fields} for data_item in data]
        
        return {key: data[key] for key in data if key in schema.model_fields}