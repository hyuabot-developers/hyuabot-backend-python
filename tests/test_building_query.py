import pytest
from async_asgi_testclient import TestClient

from query.router import graphql_schema


@pytest.mark.asyncio
async def test_building_query(
    client: TestClient,
    clean_db,
    create_test_building,
):
    query = """
        query {
            building {
                id
                name
                latitude
                longitude
                url
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["building"], list)
    assert len(response.data["building"]) > 0
    for building in response.data["building"]:  # type: dict
        assert "name" in building.keys()
        assert "latitude" in building.keys()
        assert "longitude" in building.keys()
        assert "url" in building.keys()
        assert "id" in building.keys()


@pytest.mark.asyncio
async def test_building_query_with_filter_by_location(
    client: TestClient,
    clean_db,
    create_test_building,
):
    query = """
        query {
            building(north: 90, south: 37.4, east: 90.1, west: 89.0) {
                id
                name
                latitude
                longitude
                url
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["building"], list)
    assert len(response.data["building"]) > 0
    for building in response.data["building"]:
        assert building["latitude"] <= 90
        assert building["latitude"] >= 37.4
        assert building["longitude"] <= 90.1
        assert building["longitude"] >= 89.0
        assert "name" in building.keys()
        assert "url" in building.keys()
        assert "id" in building.keys()


@pytest.mark.asyncio
async def test_building_query_with_filter_by_name(
    client: TestClient,
    clean_db,
    create_test_building,
):
    query = """
        query {
            building(name: "test") {
                id
                name
                latitude
                longitude
                url
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["building"], list)
    assert len(response.data["building"]) > 0
    for building in response.data["building"]:
        assert "test" in building["name"]
        assert "name" in building.keys()
        assert "url" in building.keys()
        assert "id" in building.keys()


@pytest.mark.asyncio
async def test_room_query(
    client: TestClient,
    clean_db,
    create_test_room,
):
    query = """
        query {
            room {
                name
                number
                latitude
                longitude
                buildingName
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["room"], list)
    assert len(response.data["room"]) > 0
    for room in response.data["room"]:
        assert "name" in room.keys()
        assert "number" in room.keys()
        assert "latitude" in room.keys()
        assert "longitude" in room.keys()
        assert "buildingName" in room.keys()


@pytest.mark.asyncio
async def test_room_query_with_filter_by_name(
    client: TestClient,
    clean_db,
    create_test_room,
):
    query = """
        query {
            room(name: "test") {
                name
                number
                latitude
                longitude
                buildingName
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["room"], list)
    assert len(response.data["room"]) > 0
    for room in response.data["room"]:
        assert "test" in room["name"]
        assert "number" in room.keys()
        assert "latitude" in room.keys()
        assert "longitude" in room.keys()
        assert "buildingName" in room.keys()


@pytest.mark.asyncio
async def test_room_query_with_filter_by_building_name(
    client: TestClient,
    clean_db,
    create_test_room,
):
    query = """
        query {
            room(buildingName: "test") {
                name
                number
                latitude
                longitude
                buildingName
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["room"], list)
    assert len(response.data["room"]) > 0
    for room in response.data["room"]:
        assert "test" in room["buildingName"]
        assert "name" in room.keys()
        assert "number" in room.keys()
        assert "latitude" in room.keys()
        assert "longitude" in room.keys()


@pytest.mark.asyncio
async def test_room_query_with_filter_by_number(
    client: TestClient,
    clean_db,
    create_test_room,
):
    query = """
        query {
            room(number: "101") {
                name
                number
                latitude
                longitude
                buildingName
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["room"], list)
    assert len(response.data["room"]) > 0
    for room in response.data["room"]:
        assert "101" in room["number"]
        assert "name" in room.keys()
        assert "latitude" in room.keys()
        assert "longitude" in room.keys()
        assert "buildingName" in room.keys()
