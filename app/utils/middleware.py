from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Response, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
import time

from app.utils.lifespan import logger
from app.utils.lifespan import get_db
from app.utils.response import DAOResponse

class SessionMiddleware(BaseHTTPMiddleware):
    async def db_session_middleware(request: Request, call_next):
        response = Response("Internal server error", status_code=500)
        try:
            request.state.db = get_db
            response = await call_next(request)
        finally:
            request.state.db.close()
        return response
        
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Prepare request log
        request_body = await request.body()
        request_log = f"{request.method} {request.url.path}"

        if request.path_params:
            request_log += f"{request.path_params}"
        if request.query_params:
            request_log += f"?{request.query_params}"
        if request_body:
            request_log += f" Body: {request_body.decode('utf-8')}"
        logger.info(f"Request: {request_log}")

        # Process request
        response = await call_next(request)
        process_time = time.time() - start_time
        response_body = b"".join([section async for section in response.body_iterator])

        # Prepare and log response
        response_log = f'"{request.method} {request.url.path} HTTP/{request.scope["http_version"]}" {response.status_code} {response_body.decode("utf-8")}'
        logger.info(f"Response: {response_log} (took {process_time:.2f} secs)")

        return Response(content=response_body, status_code=response.status_code, headers=dict(response.headers), media_type=response.media_type)

def configure_middleware(app: FastAPI):
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Content-Disposition"],
    )

    # custom handler to wrap around http response codes
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content=DAOResponse[dict](success=False, error=exc.detail).model_dump()
            # content={"success": False, "error": {"code": exc.status_code, "message": exc.detail}},
        )