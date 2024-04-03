import uvicorn
from fastapi import FastAPI

# local imports
from app.utils.lifespan import lifespan
from app.utils.middleware import configure_middleware
from app.utils.routes import configure_routes
from app.utils.settings import settings

app = FastAPI(title=settings.APP_NAME, description="", lifespan=lifespan)

# Configure middleware and routes
configure_middleware(app)
configure_routes(app)


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.APP_URL, port=8002)