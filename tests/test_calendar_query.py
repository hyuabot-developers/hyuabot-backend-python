import pytest
from async_asgi_testclient import TestClient

from query.router import graphql_schema


@pytest.mark.asyncio
async def test_calendar_query(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_calendar,
    create_test_calendar_version,
):
    query = """
        query {
            calendar {
                version,
                data {
                    category { id, name }
                    title, description, start, end
                }
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["calendar"], dict)
    calendar_data = response.data["calendar"]
    assert len(calendar_data["data"]) > 0
    for event in calendar_data["data"]:
        assert isinstance(event, dict)
        assert "category" in event.keys()
        assert "title" in event.keys()
        assert "description" in event.keys()
        assert "start" in event.keys()
        assert "end" in event.keys()
        assert "id" in event["category"].keys()
        assert "name" in event["category"].keys()


@pytest.mark.asyncio
async def test_notice_query_with_category_filter(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_calendar,
    create_test_calendar_version,
):
    query = """
        query {
            calendar (categoryId: 100) {
                version,
                data {
                    category { id, name }
                    title, description, start, end
                }
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["calendar"], dict)
    calendar_data = response.data["calendar"]
    assert len(calendar_data["data"]) > 0
    for event in calendar_data["data"]:
        assert isinstance(event, dict)
        assert "category" in event.keys()
        assert "title" in event.keys()
        assert "description" in event.keys()
        assert "start" in event.keys()
        assert "end" in event.keys()
        assert "id" in event["category"].keys()
        assert "name" in event["category"].keys()


@pytest.mark.asyncio
async def test_notice_query_with_filter_by_title(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_calendar,
    create_test_calendar_version,
):
    query = """
        query {
            calendar (title: "test") {
                version,
                data {
                    category { id, name }
                    title, description, start, end
                }
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["calendar"], dict)
    calendar_data = response.data["calendar"]
    assert len(calendar_data["data"]) > 0
    for event in calendar_data["data"]:
        assert isinstance(event, dict)
        assert "category" in event.keys()
        assert "title" in event.keys()
        assert "description" in event.keys()
        assert "start" in event.keys()
        assert "end" in event.keys()
        assert "id" in event["category"].keys()
        assert "name" in event["category"].keys()
        assert "test" in event["title"]
