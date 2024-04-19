from fastapi import APIRouter, FastAPI, Request
from app.utils.lifespan import AppLogger
from app.router.user_router import UserRouter
from app.router.role_router import RoleRouter
from app.router.permission_router import PermissionRouter

router = APIRouter()

@router.get("/logs")
@AppLogger.log_decorator
async def read_root(request: Request):
    return {"Hello": "World"}

def configure_routes(app: FastAPI):
    app.include_router(router)

    # Create an instance of UserDAO
    app.include_router(UserRouter(prefix="/users", tags=["Users"]).router)

    # Create an instance of RoleDAO
    app.include_router(RoleRouter(prefix="/roles", tags=["Roles"]).router)

    # Create an instance of PermissionDAO
    app.include_router(PermissionRouter(prefix="/permissions", tags=["Permissions"]).router)