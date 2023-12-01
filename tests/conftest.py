import asyncio
import datetime
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
        await conn.execute(text("DELETE FROM campus"))
        await conn.execute(text("DELETE FROM subway_realtime"))
        await conn.execute(text("DELETE FROM subway_timetable"))
        await conn.execute(text("DELETE FROM subway_route_station"))
        await conn.execute(text("DELETE FROM subway_route"))
        await conn.execute(text("DELETE FROM subway_station"))
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


# Campus Datas
@pytest_asyncio.fixture
async def create_test_campus() -> None:
    values = ""
    for i in range(1, 10):
        values += f"({i}, 'test_campus{i}'),"
    insert_sql = f"INSERT INTO campus VALUES {values}"[:-1]
    async with engine.begin() as conn:
        await conn.execute(text(insert_sql))


# Subway Datas
@pytest_asyncio.fixture
async def create_test_subway_station_name() -> None:
    values = ""
    for i in range(1, 10):
        values += f"('test_station_name{i}'),"
    insert_sql = f"INSERT INTO subway_station VALUES {values}"[:-1]
    async with engine.begin() as conn:
        await conn.execute(text(insert_sql))


@pytest_asyncio.fixture
async def create_test_subway_route() -> None:
    insert_sql = "INSERT INTO subway_route VALUES (1001, 'test_route')"
    async with engine.begin() as conn:
        await conn.execute(text(insert_sql))


@pytest_asyncio.fixture
async def create_test_subway_route_station(
    create_test_subway_station_name,
    create_test_subway_route,
) -> None:
    values = ""
    for i in range(1, 10):
        values += f"('K{str(i).zfill(3)}', 1001, 'test_station_name{i}', {i}, '00:{str(i).zfill(2)}:00'),"
    insert_sql = f"INSERT INTO subway_route_station VALUES {values}"[:-1]
    async with engine.begin() as conn:
        await conn.execute(text(insert_sql))


@pytest_asyncio.fixture
async def create_test_subway_timetable(
    create_test_subway_route_station,
) -> None:
    values = ""
    for i in range(1, 10):
        values += f"('K{str(i).zfill(3)}', 'K001', 'K009', '00:{str(i).zfill(2)}:00', 'weekdays', 'up'),"
        values += f"('K{str(i).zfill(3)}', 'K009', 'K001', '00:{str(i).zfill(2)}:00', 'weekdays', 'down'),"
        values += f"('K{str(i).zfill(3)}', 'K001', 'K009', '00:{str(i).zfill(2)}:00', 'weekends', 'up'),"
        values += f"('K{str(i).zfill(3)}', 'K009', 'K001', '00:{str(i).zfill(2)}:00', 'weekends', 'down'),"
    insert_sql = f"INSERT INTO subway_timetable VALUES {values}"[:-1]
    async with engine.begin() as conn:
        await conn.execute(text(insert_sql))


@pytest_asyncio.fixture
async def create_test_subway_realtime(
    create_test_subway_route_station,
) -> None:
    values = ""
    for i in range(1, 10):
        values += (
            f"('K{str(i).zfill(3)}', 0, 'K001', {i}, '00:{str(i).zfill(2)}:00', true, 'K009', "
            f"'40{str(i).zfill(2)}', '{datetime.datetime.now()}', false, false, 0),"
        )
        values += (
            f"('K{str(i).zfill(3)}', 0, 'K009', {i}, '00:{str(i).zfill(2)}:00', false, 'K001', "
            f"'40{str(i).zfill(2)}', '{datetime.datetime.now()}', false, false, 0),"
        )
    insert_sql = f"INSERT INTO subway_realtime VALUES {values}"[:-1]
    async with engine.begin() as conn:
        await conn.execute(text(insert_sql))
