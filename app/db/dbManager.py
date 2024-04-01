from app.db.dbModule import DBModule
from app.utils.settings import settings

class DBManager:
    _instance = None
    _db_module = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._db_module = None
        return cls._instance

    @property
    def db_module(self):
        return self.get_db_module()

    def initialize_db_module(self, **credentials):
        if not self._db_module:
            try:
                self._db_module = DBModule(**credentials)
            except Exception as e:
                raise RuntimeError(f"Failed to initialize DBModule: {e}")
        return self._db_module

    @classmethod
    def get_db_module(self):
        if not self._db_module:
            try:
                self.initialize_db_module(self, **self.get_credentials_from_env())
            except Exception as e:
                raise RuntimeError(f"DBModule not initialized: {e}")
        return self._db_module
    
    @staticmethod
    def get_credentials_from_env():
        user = settings.DB_USER
        password = settings.DB_PASSWORD
        host = settings.DB_HOST
        port = settings.DB_PORT
        database = settings.DB_DATABASE
        engine = settings.DB_ENGINE

        return {
            "user": user,
            "pswd": password,
            "host": host,
            "port": port,
            "db": database,
            "engine": engine,
        }
