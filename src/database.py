# Get database engine.
import datetime
from typing import AsyncGenerator, Optional

from pydantic import BaseModel
from redis.asyncio import Redis
from sqlalchemy import Select, Insert, Update, Delete
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from config import settings

# PostgreSQL database engine.
DATABASE_URL = str(settings.DATABASE_URL)
engine = create_async_engine(DATABASE_URL)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Function to get database session from any place in the application.
    Yields:
        AsyncSession: Database session.
    """
    session = AsyncSession(bind=engine)
    try:
        yield session
    finally:
        await session.close()


async def fetch_one(select_query: Select | Insert | Update):
    async with AsyncSession(engine) as session:
        query = await session.execute(select_query)
        result = query.one_or_none()
        if result:
            return result[0]
        return None


async def fetch_all(select_query: Select | Insert | Update):
    async with AsyncSession(engine) as session:
        query = await session.execute(select_query)
        return [item[0] for item in query.all()]


async def execute_query(query: Select | Insert | Update | Delete):
    async with AsyncSession(engine) as session:
        await session.execute(query)
        await session.commit()


# Redis database engine.
redis_client: Redis = None  # type: ignore


class RedisData(BaseModel):
    key: str | bytes
    value: str | bytes
    ttl: Optional[int | datetime.timedelta] = None


async def set_data(data: RedisData, is_transaction: bool = False) -> None:
    async with redis_client.pipeline(transaction=is_transaction) as pipe:
        await pipe.set(data.key, data.value)
        if data.ttl:
            await pipe.expire(data.key, data.ttl)
        await pipe.execute()


async def get_data(key: str) -> Optional[str]:
    return await redis_client.get(key)


async def delete_data(key: str) -> int:
    return await redis_client.delete(key)
