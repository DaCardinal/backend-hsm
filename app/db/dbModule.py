from functools import wraps
from typing import Any, Callable, Type,TypeVar, AsyncIterator

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy import create_engine, text

from urllib.parse import quote

import app.db.dbExceptions as DBExceptions

Base = declarative_base()

class DBModule:
    _base: Any = Base
    T = TypeVar('T', bound=Base)
    _models_generated: bool = False

    def __init__(self, **kwargs):
        self.credentials = kwargs

        # create database engine
        self.engine_type = kwargs.get("engine", "sqlite")
        self.engine_setup_func = self.get_engine_setup_func(self.engine_type)        
        self.engine: AsyncEngine = self.engine_setup_func(self.credentials)

        # create session
        self.Session: Session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine["write"], class_=AsyncSession)

    def get_engine(self):
        return self.engine
    
    def dispose(self):
        self.engine["write"].dispose()

    async def check_models_generated(self):
        if not self._models_generated:
            await self.create_all_tables()
            self._models_generated = True

    def get_engine_setup_func(cls, engine):
        supporting_rdbms = {
            "postgres": cls.setup_postgres,
            "mysql": cls.setup_mysql,
            "sqlite": cls.setup_sqlite,
            "memory": cls.setup_memory,
        }
        return supporting_rdbms.get(engine, cls.setup_sqlite)

    def setup_postgres(cls, credentials: dict):
        user = credentials.get("user")
        pswd = credentials.get("pswd", "")
        host = credentials.get("host")
        port = credentials.get("port", 3306)
        db = credentials.get("db")
        conn_string = f"postgresql+asyncpg://{user}:{quote(pswd)}@{host}:{port}/{db}"
        
        # create database if it doesn't exist
        cls.create_postgres_database_if_not_exist(conn_string)

        if not all([user, host, db]):
            raise DBExceptions.DatabaseCredentialException(
                "DB, USER and HOST are required"
            )

        return {
            "write": create_async_engine(conn_string, future=True, echo=False),
            "read": create_async_engine(conn_string, future=True, echo=False),
        }
    
    def create_postgres_database_if_not_exist(cls, database_url: str, default_database: str = "postgresql://postgres:toor@localhost/postgres"):
        engine = create_engine(default_database)
        db_name = database_url.split("/")[-1]
        conn = engine.connect()

        try:
            conn.execute(text("commit"))
            db_exists = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname='{db_name}'")).scalar()
            
            if not db_exists:
                conn.execute(text(f"CREATE DATABASE {db_name}"))
                print(f"Database {db_name} created successfully.")
            else:
                print(f"Database {db_name} already exists.")
        except SQLAlchemyError as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()
            
    def setup_mysql(cls, credentials: dict):
        user = credentials.get("user")
        pswd = credentials.get("pswd", "")
        host = credentials.get("host")
        read_host = credentials.get("read_host", host)
        port = credentials.get("port", 3306)
        db = credentials.get("db")

        if not all([user, host, db]):
            raise DBExceptions.DatabaseCredentialException(
                "DB, USER and HOST are required"
            )

        return {
            "write": create_engine(
                f"mysql+asyncmy://{user}:{quote(pswd)}@{host}:{port}/{db}",
                future=True,
                echo=False,
            ),
            "read": create_engine(
                f"mysql+asyncmy://{user}:{quote(pswd)}@{read_host}:{port}/{db}",
                future=True,
                echo=False,
            ),
        }

    def setup_memory(cls, credentials = ':memory:'):
        return {
            "write": create_engine(
                f"sqlite+pysqlite:///{credentials}", future=True, echo=True
            ),
            "read": create_engine(
                f"sqlite+pysqlite:///{credentials}", future=True, echo=True
            ),
        }

    def setup_sqlite(self, credentials = None, db_path="app.db"):
       
        return {
            "write": create_engine(
                f"sqlite+pysqlite:///{db_path}", echo=False, future=True
            ),
            "read": create_engine(
                f"sqlite+pysqlite:///{db_path}", echo=False, future=True
            ),
        }
    
    @classmethod
    def get_declarative_base(self):
        return self._base

    async def get_db(self) -> AsyncIterator[AsyncSession]:
        async with self.Session() as session:
            yield session
     
    async def create_all_tables(self):
        engine : AsyncEngine = self.engine["write"]

        async with engine.begin() as conn:
            await conn.run_sync(self._base.metadata.create_all)

    async def drop_all_tables(self):
        engine : AsyncEngine = self.engine["write"]
        async with engine.begin() as conn:
            await conn.run_sync(self._base.metadata.drop_all)

    async def add_instance(self, instance: T):
        async with self.Session() as session:
            session.add(instance)
            await session.commit()
            await session.refresh(instance)

    async def get_instances(self, model: Type[T]) -> list[T]:
        async with self.Session() as session:
            result = await session.execute(select(model))
            return result.scalars().all()
    
    async def get_instances_by_filter(self, model: Type[T], **filters) -> list[T]:
        async with self.Session() as session:
            query = select(model)
            if filters:
                query = query.filter_by(**filters)
            result = await session.execute(query)
            return result.scalars().all()

    async def update_instance(self, model: Type[T], instance_id: int, **updates):
        async with self.Session() as session:
            obj = await session.get(model, instance_id)
            if obj:
                for key, value in updates.items():
                    setattr(obj, key, value)
                await session.commit()
                return obj
            else:
                return None

    async def delete_instance(self, model: Type[T], instance_id: int):
        async with self.Session() as session:
            obj = await session.get(model, instance_id)
            if obj:
                await session.delete(obj)
                await session.commit()
                return obj
            else:
                return None

    def db_session_commit_rollback(db_session_func: Callable[..., AsyncSession]):
        @wraps(db_session_func)
        async def session_wrapper(*args, **kwargs):
            async with db_session_func(*args, **kwargs) as session:
                try:
                    response = await db_session_func(*args, session=session, **kwargs)
                    await session.commit()
                    return response
                except Exception as e:
                    await session.rollback()
                    raise e
        return session_wrapper