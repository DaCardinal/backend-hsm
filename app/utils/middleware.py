from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Response, Request
import time

from app.utils.lifespan import logger

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