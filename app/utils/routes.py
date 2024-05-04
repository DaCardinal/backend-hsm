from fastapi import APIRouter, FastAPI, Request
from app.utils.lifespan import AppLogger
from app.router import *

router = APIRouter()

def configure_routes(app: FastAPI):
    app.include_router(router)

    # Create an instance of UserDAO
    app.include_router(UserRouter(prefix="/users", tags=["Users"]).router)

    # Create an instance of RoleDAO
    app.include_router(RoleRouter(prefix="/roles", tags=["Roles"]).router)

    # Create an instance of PermissionDAO
    app.include_router(PermissionRouter(prefix="/permissions", tags=["Permissions"]).router)
    
    # Create an instance of PropertyDAO
    app.include_router(PropertyRouter(prefix="/property", tags=["Property"]).router)

    # Create an instance of PropertyDAO
    app.include_router(PropertyUnitRouter(prefix="/units", tags=["Units"]).router)

    # Create an instance of AmmenitiesDAO
    app.include_router(AmmenitiesRouter(prefix="/ammenities", tags=["Ammenities"]).router)

        # Create an instance of AmmenitiesDAO
    app.include_router(MediaRouter(prefix="/media", tags=["Media"]).router)