from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import declared_attr
from app.db.dbModule import Base

class BaseModel(Base):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def to_dict(self):
        """Converts the object instance to a Python dictionary."""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}