from importlib import import_module
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.db.dbManager import DBManager
from app.utils.logger import AppLogger
from app.factory.dataFactory import AmmenityFactory, PaymentTypesFactory, UtilitiesFactory, MediaFactory, UserFactory, RolesFactory, PermissionsFactory, RolePermissionsFactory
from app.factory.dataSeeder import DataSeeder

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

    # Import Amenities model after it's been created


    # seed ammenities model
    user_info_seeder = DataSeeder([RolesFactory(), PermissionsFactory(), RolePermissionsFactory(), UserFactory()])
    await user_info_seeder.seed_data()               
    
    seeder = DataSeeder([AmmenityFactory(), UtilitiesFactory(), PaymentTypesFactory(), MediaFactory()])
    await seeder.seed_data()

    yield

    # TODO: Add tear down items
    # await db_manager.db_module.drop_all_tables()
    logger.info("Shutting down")