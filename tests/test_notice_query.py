import pytest
from async_asgi_testclient import TestClient

from query.router import graphql_schema


@pytest.mark.asyncio
async def test_notice_query(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_notice_category,
    create_test_notice,
):
    query = """
        query {
            notice (language: "korean") {
                id, language, title, url, category { id, name }
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["notice"], list)
    assert len(response.data["notice"]) > 0
    for notice in response.data["notice"]:
        assert "id" in notice.keys()
        assert "language" in notice.keys()
        assert "title" in notice.keys()
        assert "url" in notice.keys()
        assert "category" in notice.keys()
        assert "id" in notice["category"].keys()
        assert "name" in notice["category"].keys()


@pytest.mark.asyncio
async def test_notice_query_with_category_filter(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_notice_category,
    create_test_notice,
):
    query = """
        query {
            notice (language: "korean", categoryId: 100) {
                id, language, title, url, category { id, name }
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["notice"], list)
    assert len(response.data["notice"]) > 0
    for notice in response.data["notice"]:
        assert "id" in notice.keys()
        assert "language" in notice.keys()
        assert "title" in notice.keys()
        assert "url" in notice.keys()
        assert "category" in notice.keys()
        category = notice["category"]
        assert category["id"] == 100
        assert category["name"] == "test_category100"


@pytest.mark.asyncio
async def test_notice_query_with_filter_by_title(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_notice_category,
    create_test_notice,
):
    query = """
        query {
            notice (language: "korean", title: "test") {
                id, language, title, url, category { id, name }
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["notice"], list)
    assert len(response.data["notice"]) > 0
    for notice in response.data["notice"]:
        assert "id" in notice.keys()
        assert "language" in notice.keys()
        assert "test" in notice["title"]
        assert "url" in notice.keys()
        assert "category" in notice.keys()
        assert "id" in notice["category"].keys()
        assert "name" in notice["category"].keys()
