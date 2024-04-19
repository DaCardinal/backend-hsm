from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.db.dbManager import DBManager
from app.utils.logger import AppLogger

logger = AppLogger().get_logger()

# Get DB Info
db_manager = DBManager()
get_db = db_manager.db_module.get_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # TODO: Add startup setup items
    global logger
    logger.info("Starting up")
    
    if not logger:
        app_logger = AppLogger()
        logger = app_logger.get_logger()

    # TODO: Instantiate db
    await db_manager.db_module.create_all_tables()

    yield

    # TODO: Add tear down items
    # await db_manager.db_module.drop_all_tables()
    logger.info("Shutting down")