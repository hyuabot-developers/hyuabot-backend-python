import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from async_asgi_testclient import TestClient
from sqlalchemy import text

from database import engine
from main import app
from user.security import hash_password


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[TestClient, None]:
    """Create an instance of the test client for each test case."""
    host, port = "127.0.0.1", "38000"
    scope = {"client": (host, port)}

    async with TestClient(app, scope=scope) as client:
        yield client


@pytest_asyncio.fixture
async def clean_db() -> None:
    async with engine.begin() as conn:
        await conn.execute(text("DELETE FROM auth_refresh_token"))
        await conn.execute(text("DELETE FROM admin_user"))


@pytest_asyncio.fixture
async def create_test_user() -> None:
    hashed_password = hash_password("test_password")
    async with engine.begin() as conn:
        await conn.execute(
            text(
                "INSERT INTO admin_user VALUES ("
                "'test_id', :password, 'test_name', 'test@gmail.com', 'test_phone', true)",
            ),
            {"password": hashed_password},
        )
