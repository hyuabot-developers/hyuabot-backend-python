import asyncio
import datetime
import random
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
        await conn.execute(text("DELETE FROM shuttle_timetable"))
        await conn.execute(text("DELETE FROM shuttle_route_stop"))
        await conn.execute(text("DELETE FROM shuttle_route"))
        await conn.execute(text("DELETE FROM shuttle_stop"))
        await conn.execute(text("DELETE FROM shuttle_period"))
        await conn.execute(text("DELETE FROM shuttle_period_type"))
        await conn.execute(text("DELETE FROM shuttle_holiday"))
        await conn.execute(
            text("ALTER SEQUENCE shuttle_timetable_seq_seq RESTART WITH 1"),
        )
        await conn.execute(text("DELETE FROM commute_shuttle_timetable"))
        await conn.execute(text("DELETE FROM commute_shuttle_stop"))
        await conn.execute(text("DELETE FROM commute_shuttle_route"))
        await conn.execute(text("DELETE FROM notices"))
        await conn.execute(text("DELETE FROM notice_category"))
        await conn.execute(text("DELETE FROM menu"))
        await conn.execute(text("DELETE FROM restaurant"))
        await conn.execute(text("DELETE FROM reading_room"))
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


# Cafeteria Datas
@pytest_asyncio.fixture
async def create_test_cafeteria(create_test_campus) -> None:
    values = ""
    for i in range(1, 10):
        values += f"({i // 5 + 1}, {i}, 'test_cafeteria{i}', 89.0, 89.0),"
    insert_sql = f"INSERT INTO restaurant VALUES {values}"[:-1]
    async with engine.begin() as conn:
        await conn.execute(text(insert_sql))


@pytest_asyncio.fixture
async def create_test_cafeteria_menu(create_test_cafeteria) -> None:
    values = "(1, '2023-12-01', '조식', 'test_menu', 'test_price'),"
    types = ["조식", "중식", "석식"]
    for i in range(1, 10):
        for j in range(-5, 5):
            feed_date = datetime.datetime.now().date() + datetime.timedelta(days=j)
            values += f"({i}, '{feed_date}', '{random.choice(types)}', 'test_menu{i}', 'test_price'),"
    insert_sql = f"INSERT INTO menu VALUES {values}"[:-1]
    async with engine.begin() as conn:
        await conn.execute(text(insert_sql))


# Commute Shuttle Datas
@pytest_asyncio.fixture
async def create_test_commute_shuttle_route() -> None:
    values = ""
    for i in range(1, 10):
        values += f"('test_route{i}', 'test_description{i}', 'test_description{i}'),"
    insert_sql = f"INSERT INTO commute_shuttle_route VALUES {values}"[:-1]
    async with engine.begin() as conn:
        await conn.execute(text(insert_sql))


@pytest_asyncio.fixture
async def create_test_commute_shuttle_stop() -> None:
    values = ""
    for i in range(1, 50):
        values += f"('test_stop{i}', 'test_description{i}', 89.9, 89.9),"
    insert_sql = f"INSERT INTO commute_shuttle_stop VALUES {values}"[:-1]
    async with engine.begin() as conn:
        await conn.execute(text(insert_sql))


@pytest_asyncio.fixture
async def create_test_commute_shuttle_timetable(
    create_test_commute_shuttle_route,
    create_test_commute_shuttle_stop,
) -> None:
    values = ""
    for i in range(1, 50):
        values += f"('test_route{(i // 10 + 1)}', 'test_stop{i}', {i}, '07:{str(i).zfill(2)}:00'),"
    insert_sql = f"INSERT INTO commute_shuttle_timetable VALUES {values}"[:-1]
    async with engine.begin() as conn:
        await conn.execute(text(insert_sql))


# Notice Datas
@pytest_asyncio.fixture
async def create_test_notice_category() -> None:
    values = ""
    for i in range(100, 110):
        values += f"({i}, 'test_category{i}'),"
    insert_sql = f"INSERT INTO notice_category VALUES {values}"[:-1]
    async with engine.begin() as conn:
        await conn.execute(text(insert_sql))


@pytest_asyncio.fixture
async def create_test_notice(create_test_notice_category, create_test_user) -> None:
    values = ""
    for i in range(9999, 10000):
        values += f"({i}, 'test_title{i}', 'test_url', '2023-12-01T23:59:59', 100, 'test_id'),"
    insert_sql = f"INSERT INTO notices VALUES {values}"[:-1]
    async with engine.begin() as conn:
        await conn.execute(text(insert_sql))


# Reading Room Datas
@pytest_asyncio.fixture
async def create_test_reading_room(create_test_campus) -> None:
    values = ""
    for i in range(1, 10):
        values += (
            f"({i % 2 + 1}, {i}, 'test_reading_room{i}', true, true, 100, 100, 0),"
        )
    insert_sql = f"INSERT INTO reading_room VALUES {values}"[:-1]
    async with engine.begin() as conn:
        await conn.execute(text(insert_sql))


# Shuttle Datas
@pytest_asyncio.fixture
async def create_test_shuttle_period_type() -> None:
    types = ["semester", "vacation", "vacation_session"]
    values = ""
    for i in types:
        values += f"('{i}'),"
    insert_sql = f"INSERT INTO shuttle_period_type VALUES {values}"[:-1]
    async with engine.begin() as conn:
        await conn.execute(text(insert_sql))


@pytest_asyncio.fixture
async def create_test_shuttle_period(create_test_shuttle_period_type) -> None:
    types = ["semester", "vacation", "vacation_session"]
    start = datetime.datetime.combine(
        datetime.datetime.now() - datetime.timedelta(days=365),
        datetime.datetime.min.time(),
    )
    values = "('semester', '2021-12-01 00:00:00+09:00', '2022-12-01 23:59:59+09:00'),"
    for i in range(1, 10):
        end = datetime.datetime.combine(
            start + datetime.timedelta(days=random.randint(1, 30)),
            datetime.datetime.max.time(),
        )
        values += f"('{random.choice(types)}', '{start}+09:00', '{end}+09:00'),"
        start = datetime.datetime.combine(
            end + datetime.timedelta(days=1),
            datetime.datetime.min.time(),
        )

    insert_sql = f"INSERT INTO shuttle_period VALUES {values}"[:-1]
    async with engine.begin() as conn:
        await conn.execute(text(insert_sql))


@pytest_asyncio.fixture
async def create_test_shuttle_holiday() -> None:
    start_date = datetime.datetime.now().date()
    types = ["weekends", "halt"]
    values = ""
    for i in range(1, 10):
        values += f"('{start_date}', '{random.choice(types)}', 'solar'),"
        start_date += datetime.timedelta(days=random.randint(1, 30))
    insert_sql = f"INSERT INTO shuttle_holiday VALUES {values}"[:-1]
    async with engine.begin() as conn:
        await conn.execute(text(insert_sql))


@pytest_asyncio.fixture
async def create_test_shuttle_stop() -> None:
    values = ""
    for i in range(1, 10):
        values += f"('test_stop{i}', 89.9, 89.9),"
    insert_sql = f"INSERT INTO shuttle_stop VALUES {values}"[:-1]
    async with engine.begin() as conn:
        await conn.execute(text(insert_sql))


@pytest_asyncio.fixture
async def create_test_shuttle_route(create_test_shuttle_stop) -> None:
    values = ""
    for i in range(1, 10):
        values += (
            f"('test_route{i}', 'test_description{i}', 'test_description{i}',"
            "'test_tag', 'test_stop1', 'test_stop2'),"
        )
    insert_sql = f"INSERT INTO shuttle_route VALUES {values}"[:-1]
    async with engine.begin() as conn:
        await conn.execute(text(insert_sql))


@pytest_asyncio.fixture
async def create_test_shuttle_route_stop(create_test_shuttle_route) -> None:
    values = ""
    for i in range(1, 10):
        values += f"('test_route{i}', 'test_stop{i}', {i}, '00:0{i}:00'),"
    insert_sql = f"INSERT INTO shuttle_route_stop VALUES {values}"[:-1]
    async with engine.begin() as conn:
        await conn.execute(text(insert_sql))


@pytest_asyncio.fixture
async def create_test_shuttle_timetable(
    create_test_shuttle_period,
    create_test_shuttle_route,
) -> None:
    values = ""
    for i in range(1, 10):
        values += f"({i}, 'semester', true, 'test_route1', '0{i}:00+09:00'),"
    insert_sql = f"INSERT INTO shuttle_timetable VALUES {values}"[:-1]
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
