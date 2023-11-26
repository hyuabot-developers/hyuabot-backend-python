# Get database engine.
import datetime
from typing import AsyncGenerator, Optional

from redis.asyncio import Redis
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


# Redis database engine.
redis_client: Redis = None  # type: ignore


class RedisData:
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
