from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, APIRouter
from query.router import graphql_router
from redis.asyncio import ConnectionPool, Redis
from starlette.middleware.cors import CORSMiddleware

import database
from building.router import router as building_router
from bus.router import router as bus_router
from cafeteria.router import router as cafeteria_router
from campus.router import router as campus_router
from commute_shuttle.router import router as commute_shuttle_router
from config import app_configs, settings
from contact.router import router as contact_router
from event.router import router as calendar_router
from notice.router import router as notice_router
from reading_room.router import router as reading_room_router
from shuttle.router import router as shuttle_router
from subway.router import router as subway_router
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
api.include_router(bus_router, prefix="/bus", tags=["bus"])
api.include_router(cafeteria_router, prefix="/cafeteria", tags=["cafeteria"])
api.include_router(building_router, prefix="/building", tags=["building"])
api.include_router(campus_router, prefix="/campus", tags=["campus"])
api.include_router(commute_shuttle_router, prefix="/commute", tags=["commute-shuttle"])
api.include_router(notice_router, prefix="/notice", tags=["notice"])
api.include_router(reading_room_router, prefix="/library", tags=["reading-room"])
api.include_router(shuttle_router, prefix="/shuttle", tags=["shuttle"])
api.include_router(subway_router, prefix="/subway", tags=["subway"])
api.include_router(calendar_router, prefix="/calendar", tags=["calendar"])
api.include_router(contact_router, prefix="/contact", tags=["contact"])
api.include_router(auth_router, prefix="/auth")
app.include_router(api, prefix="/api")
app.include_router(graphql_router, prefix="/query")


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
