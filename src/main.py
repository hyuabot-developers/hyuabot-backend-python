from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, APIRouter
from redis.asyncio import ConnectionPool, Redis
from starlette.middleware.cors import CORSMiddleware

import database
from config import app_configs, settings
from user.router import router as auth_router


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncGenerator:
    # Startup
    redis_pool = ConnectionPool.from_url(
        str(settings.REDIS_URL),
        decode_responses=True,
        max_connections=100,
    )
    database.redis_client = Redis(connection_pool=redis_pool)
    yield

    if settings.ENVIRONMENT.is_testing:
        return

    # Shutdown
    await redis_pool.disconnect()


app = FastAPI(**app_configs, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
    allow_headers=settings.CORS_HEADERS,
)

# API routes
api = APIRouter()
api.include_router(auth_router, prefix="/auth")
app.include_router(api, prefix="/api")


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
