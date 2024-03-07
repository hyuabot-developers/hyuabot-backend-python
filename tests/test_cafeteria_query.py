import pytest
from async_asgi_testclient import TestClient

from query.router import graphql_schema


@pytest.mark.asyncio
async def test_get_cafeteria_query(
    client: TestClient,
    clean_db,
    create_test_cafeteria_menu,
) -> None:
    query = """
        query {
            menu {
                id, name, latitude, longitude,
                menu {
                    date, type, menu, price
                }
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["menu"], list)
    for cafeteria in response.data["menu"]:
        assert "id" in cafeteria.keys()
        assert "name" in cafeteria.keys()
        assert "latitude" in cafeteria.keys()
        assert "longitude" in cafeteria.keys()
        assert "menu" in cafeteria.keys()
        for menu in cafeteria["menu"]:
            assert "date" in menu.keys()
            assert "type" in menu.keys()
            assert "menu" in menu.keys()
            assert "price" in menu.keys()


@pytest.mark.asyncio
async def test_get_cafeteria_query_campus_filter(
    client: TestClient,
    clean_db,
    create_test_cafeteria_menu,
) -> None:
    query = """
        query {
            menu (campusId: 2) {
                id, name, latitude, longitude,
                menu {
                    date, type, menu, price
                }
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["menu"], list)
    for cafeteria in response.data["menu"]:
        assert "id" in cafeteria.keys()
        assert "name" in cafeteria.keys()
        assert "latitude" in cafeteria.keys()
        assert "longitude" in cafeteria.keys()
        assert "menu" in cafeteria.keys()
        for menu in cafeteria["menu"]:
            assert "date" in menu.keys()
            assert "type" in menu.keys()
            assert "menu" in menu.keys()
            assert "price" in menu.keys()


@pytest.mark.asyncio
async def test_get_cafeteria_query_name_filter(
    client: TestClient,
    clean_db,
    create_test_cafeteria_menu,
) -> None:
    query = """
        query {
            menu (name: "test_cafeteria1") {
                id, name, latitude, longitude,
                menu {
                    date, type, menu, price
                }
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["menu"], list)
    for cafeteria in response.data["menu"]:
        assert cafeteria["name"] == "test_cafeteria1"


@pytest.mark.asyncio
async def test_get_cafeteria_query_date_filter(
    client: TestClient,
    clean_db,
    create_test_cafeteria_menu,
) -> None:
    query = """
        query {
            menu (date: "2023-12-01") {
                id, name, latitude, longitude,
                menu {
                    date, type, menu, price
                }
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["menu"], list)
    for cafeteria in response.data["menu"]:
        if cafeteria["id"] == 1:
            assert len(cafeteria["menu"]) > 0
            for menu in cafeteria["menu"]:
                assert menu["date"] == "2023-12-01"


@pytest.mark.asyncio
async def test_get_cafeteria_query_type_filter(
    client: TestClient,
    clean_db,
    create_test_cafeteria_menu,
) -> None:
    query = """
        query {
            menu (type_: ["조식", "중식"]) {
                id, name, latitude, longitude,
                menu {
                    date, type, menu, price
                }
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["menu"], list)
    for cafeteria in response.data["menu"]:
        assert len(cafeteria["menu"]) > 0
        for menu in cafeteria["menu"]:
            assert menu["type"] in ["조식", "중식"]
