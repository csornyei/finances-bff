import time
import os
import httpx
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request

from finances_bff.logger import logger
from finances_bff.routes.account import router as account_router
from finances_bff.routes.file import router as file_router
from finances_bff.routes.health import router as health_router
from finances_bff.routes.statement import router as statement_router
from finances_bff.routes.tag import router as tag_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    tag_service_url = os.getenv("TAG_SERVICE_URL")
    if not tag_service_url:
        raise ValueError("TAG_SERVICE_URL environment variable is not set")
    app.state.tag_service_client = httpx.AsyncClient(base_url=tag_service_url)

    statement_service_url = os.getenv("STATEMENT_SERVICE_URL")
    if not statement_service_url:
        raise ValueError("STATEMENT_SERVICE_URL environment variable is not set")
    app.state.statement_service_client = httpx.AsyncClient(
        base_url=statement_service_url
    )

    account_service_url = os.getenv("ACCOUNT_SERVICE_URL")
    if not account_service_url:
        raise ValueError("ACCOUNT_SERVICE_URL environment variable is not set")
    app.state.account_service_client = httpx.AsyncClient(base_url=account_service_url)

    file_service_url = os.getenv("FILE_SERVICE_URL")
    if not file_service_url:
        raise ValueError("FILE_SERVICE_URL environment variable is not set")
    app.state.file_service_client = httpx.AsyncClient(base_url=file_service_url)

    yield


app = FastAPI(
    lifespan=lifespan,
    openapi_tags=[
        {"name": "health", "description": "Health check endpoints"},
        {"name": "account", "description": "Account management endpoints"},
        {"name": "file", "description": "File management endpoints"},
        {"name": "statement", "description": "Statement management endpoints"},
        {"name": "tag", "description": "Tag management endpoints"},
    ],
)


@app.middleware("http")
async def log_response(request: Request, call_next):
    """
    Middleware to log request and response details.
    """
    start_time = time.perf_counter()
    data = {
        "url": str(request.url),
        "method": request.method,
        "headers": dict(request.headers),
    }
    response = await call_next(request)

    process_time = time.perf_counter() - start_time
    data["process_time"] = process_time
    data["response"] = {
        "status_code": response.status_code,
        "headers": dict(response.headers),
    }

    logger.info(data)

    return response


@app.middleware("http")
async def handle_exceptions(request: Request, call_next):
    """
    Middleware to handle exceptions and log them.
    """
    try:
        response = await call_next(request)
        return response
    except HTTPException as http_exception:
        logger.error(f"HTTP exception: {http_exception.detail}")
        return {"error": http_exception.detail}, http_exception.status_code
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
        return {"error": "Internal Server Error"}, 500


app.include_router(account_router, prefix="/api/v1", tags=["account"])
app.include_router(file_router, prefix="/api/v1", tags=["file"])
app.include_router(statement_router, prefix="/api/v1", tags=["statement"])
app.include_router(tag_router, prefix="/api/v1", tags=["tag"])
app.include_router(health_router, tags=["health"])
