from uuid import UUID
from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.asyncio import AsyncAttrs
from datetime import datetime

from app.db.dbModule import Base

class BaseModel(AsyncAttrs, Base):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    # def to_dict(self, exclude=None):
        # """Converts the object instance to a Python dictionary."""
        # data = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        # return data
    
    def to_dict(self, exclude=None):
        if exclude is None:
            exclude = set()
        data = {}

        for key in self.__dict__.keys():
            if not key.startswith("_") and key not in exclude:
                value = getattr(self, key)
                if isinstance(value, datetime):
                    value = str(value)
                if isinstance(value, UUID):
                    value = str(value)
                data[key] = value

        return data