from datetime import datetime

# from sqlalchemy.ext.asyncio import AsyncAttrs
import pytz
from sqlalchemy import Column, DateTime, UUID
from sqlalchemy.ext.declarative import declared_attr

from app.db.dbDeclarative import Base


class BaseModel(Base):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(pytz.utc))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(pytz.utc),
        onupdate=datetime.now(pytz.utc),
    )

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
