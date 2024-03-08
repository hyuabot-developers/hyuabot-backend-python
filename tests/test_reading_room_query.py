import pytest
from async_asgi_testclient import TestClient

from query.router import graphql_schema


@pytest.mark.asyncio
async def test_get_reading_room_query(
    client: TestClient,
    clean_db,
    create_test_reading_room,
) -> None:
    query = """
        query {
            readingRoom {
                id,
                name,
                isActive,
                total,
                active,
                occupied,
                available,
                updatedAt
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["readingRoom"], list)
    for cafeteria in response.data["readingRoom"]:
        assert "id" in cafeteria.keys()
        assert "name" in cafeteria.keys()
        assert "isActive" in cafeteria.keys()
        assert "total" in cafeteria.keys()
        assert "active" in cafeteria.keys()
        assert "occupied" in cafeteria.keys()
        assert "available" in cafeteria.keys()
        assert "updatedAt" in cafeteria.keys()


@pytest.mark.asyncio
async def test_get_reading_room_query_campus_filter(
    client: TestClient,
    clean_db,
    create_test_reading_room,
) -> None:
    query = """
        query {
            readingRoom (campusId: 1) {
                id,
                name,
                isActive,
                total,
                active,
                occupied,
                available,
                updatedAt
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["readingRoom"], list)
    for cafeteria in response.data["readingRoom"]:
        assert "id" in cafeteria.keys()
        assert "name" in cafeteria.keys()
        assert "isActive" in cafeteria.keys()
        assert "total" in cafeteria.keys()
        assert "active" in cafeteria.keys()
        assert "occupied" in cafeteria.keys()
        assert "available" in cafeteria.keys()
        assert "updatedAt" in cafeteria.keys()


@pytest.mark.asyncio
async def test_get_reading_room_query_name_filter(
    client: TestClient,
    clean_db,
    create_test_reading_room,
) -> None:
    query = """
        query {
            readingRoom (name: "test_reading_room1") {
                id,
                name,
                isActive,
                total,
                active,
                occupied,
                available,
                updatedAt
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["readingRoom"], list)
    for cafeteria in response.data["readingRoom"]:
        assert cafeteria["name"] == "test_reading_room1"


@pytest.mark.asyncio
async def test_get_reading_room_query_active_filter(
    client: TestClient,
    clean_db,
    create_test_reading_room,
) -> None:
    query = """
        query {
            readingRoom (isActive: true) {
                id,
                name,
                isActive,
                total,
                active,
                occupied,
                available,
                updatedAt
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["readingRoom"], list)
    for cafeteria in response.data["readingRoom"]:
        assert cafeteria["isActive"] is True


@pytest.mark.asyncio
async def test_get_reading_room_query_inactive_filter(
    client: TestClient,
    clean_db,
    create_test_reading_room,
) -> None:
    query = """
        query {
            readingRoom (isActive: false) {
                id,
                name,
                isActive,
                total,
                active,
                occupied,
                available,
                updatedAt
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["readingRoom"], list)
    for cafeteria in response.data["readingRoom"]:
        assert cafeteria["isActive"] is False
