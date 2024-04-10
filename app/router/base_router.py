from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from typing import Generic, TypeVar, List

from app.dao.base_dao import BaseDAO
from app.utils.lifespan import get_db
from app.schema.base_schema import SchemasDictType

DBModelType = TypeVar("DBModelType")

class BaseCRUDRouter(Generic[DBModelType]):
    def __init__(
        self,
        dao: BaseDAO[DBModelType],
        schemas: SchemasDictType,
        prefix: str = "",
        tags: List[str] = []
    ):
        self.model_schema = schemas["model_schema"]
        self.create_schema = schemas["create_schema"]
        self.update_schema = schemas["update_schema"]
        self.model_pk = schemas["primary_keys"]
        self.router = APIRouter(prefix=prefix, tags=tags)
        self.dao = dao
        self.get_db = get_db
        
        self.add_get_all_route()
        self.add_get_route()
        self.add_create_route()
        self.add_update_route()
        self.add_delete_route()
    
    def get_session_db(request: Request):
        return request.state.db

    def add_get_all_route(self):
        @self.router.get("/")
        async def get_all(db: Session = Depends(self.get_db)):
            item = await self.dao.get_all(db_session=db)
            if item is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No items found")
            return item

    def add_get_route(self):
        @self.router.get("/{id}")
        async def get(id: UUID, db: Session = Depends(self.get_db)):
            item = await self.dao.query(db_session=db, filters={f"{self.model_pk[0]}": id}, single=True)
            if item is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
            return item

    def add_create_route(self):
        @self.router.post("/", status_code=status.HTTP_201_CREATED)
        async def create(item: self.create_schema, db: Session = Depends(self.get_db)):
            try:
                return await self.dao.create(db_session=db, obj_in=item.dict())
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def add_update_route(self):
        @self.router.put("/{id}")
        async def update(id: UUID, item: self.create_schema, db: Session = Depends(self.get_db)):
            db_item = await self.dao.query(db_session=db, filters={f"{self.model_pk[0]}": id}, single=True)
            if not db_item:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
            try:
                return await self.dao.update(db_session=db, db_obj=db_item, obj_in=item)
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def add_delete_route(self):
        @self.router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
        async def delete(id: UUID, db: Session = Depends(self.get_db)):
            db_item = await self.dao.query(db_session=db, filters={f"{self.model_pk[0]}": id}, single=True)

            if not db_item:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
            
            try:
                await self.dao.delete(db_session=db, db_obj=db_item)
                return {"detail": "Item deleted successfully"}
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))