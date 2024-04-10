from fastapi import APIRouter, FastAPI, Request
from app.utils.lifespan import AppLogger
from app.router.user_router import UserRouter
from app.router.role_router import RoleRouter

router = APIRouter()

@router.get("/logs")
@AppLogger.log_decorator
async def read_root(request: Request):
    return {"Hello": "World"}

def configure_routes(app: FastAPI):
    app.include_router(router)

    # Create an instance of UserDAO
    user_router = UserRouter(prefix="/users", tags=["Users"])
    app.include_router(user_router.router)

    # Create an instance of RoleDAO
    user_router = RoleRouter(prefix="/roles", tags=["Roles"])
    app.include_router(user_router.router)