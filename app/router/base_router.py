from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, List, TypeVar, Generic, Optional
from pydantic import BaseModel, create_model
from sqlalchemy import inspect

from app.dao.base_dao import BaseDAO
from app.utils.response import DAOResponse
from app.utils.lifespan import get_db
from app.schema.base_schema import SchemasDictType

DBModelType = TypeVar("DBModelType")


class CustomBaseModel(BaseModel):
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

def decompose_dict(d):
    # Helper function to check if a value is an instance of a class with a to_dict method
    def is_class_instance_with_to_dict(val):
        return hasattr(val, 'to_dict') and callable(getattr(val, 'to_dict'))

    # If the input is a dictionary, process each key-value pair
    if isinstance(d, dict):
        decomposed = {}
        for key, value in d.items():
            if is_class_instance_with_to_dict(value):
                decomposed[key] = value.to_dict()
            elif isinstance(value, dict):
                decomposed[key] = decompose_dict(value)
            elif isinstance(value, list):
                decomposed[key] = [decompose_dict(item.to_dict()) for item in value]
            else:
                decomposed[key] = value
        return decomposed
    # If the input is a list, process each item in the list
    elif isinstance(d, list):
        return [decompose_dict(item) for item in d]
    # If the input is neither a dictionary nor a list, return it as is
    else:
        return d

def create_pydantic_model_from_sqlalchemy(sqlalchemy_model, load_parent_relationships = False, load_child_relationships = False, visited_models=None, excludes = [], level = 0):
    if visited_models is None:
        visited_models = {}

    model_name = sqlalchemy_model.__name__ + 'Model'

    if model_name in visited_models:
        return visited_models[model_name]

    pydantic_model = create_model(model_name)
    visited_models[model_name] = pydantic_model

    fields = {}
    default_excludes = ['created_at', 'updated_at'] + excludes

    for column in sqlalchemy_model.__table__.columns:
        if column.name not in default_excludes:
            field_type = (Optional[column.type.python_type], None)
            fields[column.name] = field_type

    if load_parent_relationships:
        level += 1
        
        if not load_child_relationships and level > 0:
            load_parent_relationships = False
            load_child_relationships = False

        for relationship in inspect(sqlalchemy_model).relationships:
            if relationship.lazy != 'dynamic' and relationship.key not in default_excludes:
                sub_model = create_pydantic_model_from_sqlalchemy(relationship.mapper.class_, load_parent_relationships,load_child_relationships, visited_models, excludes, level)
                relationship_type = List[sub_model] if relationship.uselist else sub_model
                fields[relationship.key] = (Optional[relationship_type], ...)

    pydantic_model = create_model(model_name, **fields, __base__=CustomBaseModel)
    visited_models[model_name] = pydantic_model

    return pydantic_model

class BaseCRUDRouter(Generic[DBModelType]):
    def __init__(
        self,
        dao: BaseDAO[DBModelType],
        schemas: SchemasDictType,
        prefix: str = "",
        tags: List[str] = [], show_default_routes = True
    ):
        self.model_schema = schemas["model_schema"]
        self.create_schema = schemas["create_schema"]
        self.update_schema = schemas["update_schema"]
        self.model_pk = schemas["primary_keys"]
        self.router = APIRouter(prefix=prefix, tags=tags)
        self.dao = dao
        self.get_db = get_db
        
        if show_default_routes:
            self.add_get_all_route()
            self.add_get_route()
            self.add_create_route()
            self.add_update_route()
            self.add_delete_route()
    
    def get_session_db(request: Request):
        return request.state.db

    def add_get_all_route(self):
        @self.router.get("/")
        async def get_all(db: AsyncSession = Depends(self.get_db)):
            items = await self.dao.get_all(db_session=db)
            if items is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No items found")
            
            dynamic_model = create_pydantic_model_from_sqlalchemy(self.dao.model, load_parent_relationships=self.dao.load_parent_relationships, load_child_relationships=self.dao.load_child_relationships, excludes=self.dao.excludes)

            if self.dao.load_child_relationships:
                return DAOResponse[List[Any]](success=True, data=[decompose_dict(item.to_dict()) for item in items])

            return items if isinstance(items, DAOResponse) or self.dao.load_child_relationships else DAOResponse[Any](success=True, data=[dynamic_model.model_validate(item, strict=False, from_attributes=True) for item in items])
            
    def add_get_route(self):
        @self.router.get("/{id}")
        async def get(id: UUID, db: AsyncSession = Depends(self.get_db)) -> DAOResponse:
            # item = await self.dao.query(db_session=db, filters={f"{self.model_pk[0]}": id}, single=True)
            item = await self.dao.get(db_session=db, id=id)

            if item is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
            
            dynamic_model = create_pydantic_model_from_sqlalchemy(self.dao.model, load_parent_relationships=self.dao.load_parent_relationships, load_child_relationships=self.dao.load_child_relationships, excludes=self.dao.excludes)

            if self.dao.load_child_relationships:
                return DAOResponse[Any](success=True, data=decompose_dict(item.to_dict()))
            
            return item if isinstance(item, DAOResponse) else DAOResponse[Any](success=True, data=dynamic_model.model_validate(item, strict=False, from_attributes=True))

    def add_create_route(self):
        @self.router.post("/", status_code=status.HTTP_201_CREATED)
        async def create(item: self.create_schema, db: AsyncSession = Depends(self.get_db)) -> DAOResponse:
            try:
                return await self.dao.create(db_session=db, obj_in=item.dict())
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def add_update_route(self):
        @self.router.put("/{id}")
        async def update(id: UUID, item: self.update_schema, db: AsyncSession = Depends(self.get_db)) -> DAOResponse:
            db_item = await self.dao.query(db_session=db, filters={f"{self.model_pk[0]}": id}, single=True)
            if not db_item:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
            try:
                item = await self.dao.update(db_session=db, db_obj=db_item, obj_in=item)

                return item if isinstance(item, DAOResponse) else DAOResponse[Any](success=True, data=item.to_dict())
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def add_delete_route(self):
        @self.router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
        async def delete(id: UUID, db: AsyncSession = Depends(self.get_db)):
            db_item = await self.dao.query(db_session=db, filters={f"{self.model_pk[0]}": id}, single=True)

            if not db_item:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
            
            try:
                await self.dao.delete(db_session=db, db_obj=db_item)
                return {"detail": "Item deleted successfully"}
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))