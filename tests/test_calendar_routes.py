import pytest
from async_asgi_testclient import TestClient
from sqlalchemy import select

from database import fetch_one
from model.calendar import CalendarCategory, Calendar
from tests.utils import get_access_token


@pytest.mark.asyncio
async def test_get_calendar_category_list(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_calendar_category,
) -> None:
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/calendar/category",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("data") is not None
    assert len(response_json["data"]) > 0
    for calendar_category in response_json["data"]:
        assert calendar_category.get("id") is not None
        assert calendar_category.get("name") is not None


@pytest.mark.asyncio
async def test_get_calendar_category_list_filter(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_calendar_category,
) -> None:
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/calendar/category?name=test_category",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("data") is not None
    assert len(response_json["data"]) > 0
    for calendar_category in response_json["data"]:
        assert calendar_category.get("id") is not None
        assert "test_category" in calendar_category.get("name")


@pytest.mark.asyncio
async def test_create_calendar_category(
    client: TestClient,
    clean_db,
    create_test_user,
) -> None:
    access_token = await get_access_token(client)
    response = await client.post(
        "/api/calendar/category",
        json={"name": "test_category"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 201
    response_json = response.json()
    assert response_json.get("id") is not None
    assert response_json.get("name") is not None
    assert response_json["name"] == "test_category"
    check_statement = select(CalendarCategory).where(
        CalendarCategory.name == "test_category",
    )
    query_result = await fetch_one(check_statement)
    assert query_result is not None
    assert query_result.name == "test_category"


@pytest.mark.asyncio
async def test_create_calendar_category_duplicated_name(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_calendar_category,
) -> None:
    access_token = await get_access_token(client)
    response = await client.post(
        "/api/calendar/category",
        json={"name": "test_category100"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "DUPLICATE_CATEGORY_NAME"}


@pytest.mark.asyncio
async def test_create_calendar_category_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_calendar_category,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from event import service

    async def mock_create_calendar_category(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "create_calendar_category", mock_create_calendar_category)

    access_token = await get_access_token(client)
    response = await client.post(
        "/api/calendar/category",
        json={"name": "test_category"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 500
    assert response.json() == {"detail": "INTERNAL_SERVER_ERROR"}


@pytest.mark.asyncio
async def test_update_calendar_category(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_calendar_category,
) -> None:
    access_token = await get_access_token(client)
    response = await client.put(
        "/api/calendar/category/100",
        json={"name": "test_category"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("id") == 100
    assert response_json.get("name") == "test_category"
    check_statement = select(CalendarCategory).where(
        CalendarCategory.name == "test_category",
    )
    query_result = await fetch_one(check_statement)
    assert query_result is not None
    assert query_result.name == "test_category"


@pytest.mark.asyncio
async def test_get_calendar_category(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_calendar_category,
) -> None:
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/calendar/category/100",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("id") == 100
    assert response_json.get("name") == "test_category100"


@pytest.mark.asyncio
async def test_get_calendar_category_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_calendar_category,
) -> None:
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/calendar/category/1000",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "CATEGORY_NOT_FOUND"}


@pytest.mark.asyncio
async def test_delete_calendar_category(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_calendar_category,
) -> None:
    access_token = await get_access_token(client)
    response = await client.delete(
        "/api/calendar/category/100",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_calendar_category_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_calendar_category,
) -> None:
    access_token = await get_access_token(client)
    response = await client.delete(
        "/api/calendar/category/1000",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "CATEGORY_NOT_FOUND"}


@pytest.mark.asyncio
async def test_get_calendar_list(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_calendar_category,
    create_test_calendar,
) -> None:
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/calendar/100/category/event",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("data") is not None
    assert len(response_json["data"]) > 0
    for calendar in response_json["data"]:
        assert calendar.get("id") is not None
        assert calendar.get("title") is not None
        assert calendar.get("description") is not None
        assert calendar.get("start") is not None
        assert calendar.get("end") is not None


@pytest.mark.asyncio
async def test_get_calendar_list_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_calendar_category,
    create_test_calendar,
) -> None:
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/calendar/category/1000/event",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "CATEGORY_NOT_FOUND"}


@pytest.mark.asyncio
async def test_get_calendar(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_calendar_category,
    create_test_calendar,
) -> None:
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/calendar/category/100/event/9999",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("id") == 9999
    assert response_json.get("title") == "test_title9999"
    assert response_json.get("description") == "test_description"
    assert response_json.get("start") is not None
    assert response_json.get("end") is not None


@pytest.mark.asyncio
async def test_get_calendar_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_calendar_category,
    create_test_calendar,
) -> None:
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/calendar/category/100/event/100",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "CALENDAR_NOT_FOUND"}


@pytest.mark.asyncio
async def test_create_calendar(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_calendar_category,
) -> None:
    access_token = await get_access_token(client)
    response = await client.post(
        "/api/calendar/category/100/event",
        json={
            "title": "test_title",
            "description": "test_description",
            "start": "2021-07-31",
            "end": "2021-07-31",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 201
    response_json = response.json()
    assert response_json.get("id") is not None
    assert response_json.get("title") == "test_title"
    assert response_json.get("description") == "test_description"
    assert response_json.get("start") is not None
    assert response_json.get("end") is not None
    check_statement = select(Calendar).where(
        Calendar.title == "test_title",
    )
    query_result = await fetch_one(check_statement)
    assert query_result is not None
    assert query_result.title == "test_title"


@pytest.mark.asyncio
async def test_create_calendar_category_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_calendar_category,
) -> None:
    access_token = await get_access_token(client)
    response = await client.post(
        "/api/calendar/category/1000/event",
        json={
            "title": "test_title",
            "description": "test_description",
            "start": "2021-07-31",
            "end": "2021-07-31",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "CATEGORY_NOT_FOUND"}


@pytest.mark.asyncio
async def test_create_calendar_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_calendar_category,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from event import service

    async def mock_create_calendar(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "create_calendar", mock_create_calendar)

    access_token = await get_access_token(client)
    response = await client.post(
        "/api/calendar/category/100/event",
        json={
            "title": "test_title",
            "description": "test_description",
            "start": "2021-07-31",
            "end": "2021-07-31",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 500
    assert response.json() == {"detail": "INTERNAL_SERVER_ERROR"}


@pytest.mark.asyncio
async def test_delete_calendar(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_calendar_category,
    create_test_calendar,
) -> None:
    access_token = await get_access_token(client)
    response = await client.delete(
        "/api/calendar/category/100/event/100",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_update_calendar(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_calendar_category,
    create_test_calendar,
) -> None:
    access_token = await get_access_token(client)
    response = await client.put(
        "/api/calendar/category/100/event/9999",
        json={
            "title": "test_title",
            "description": "test_description",
            "start": "2021-07-31",
            "end": "2021-07-31",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("id") is not None
    assert response_json.get("title") == "test_title"
    assert response_json.get("description") == "test_description"
    assert response_json.get("start") is not None
    assert response_json.get("end") is not None


@pytest.mark.asyncio
async def test_update_calendar_category_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_calendar_category,
    create_test_calendar,
) -> None:
    access_token = await get_access_token(client)
    response = await client.put(
        "/api/calendar/category/1000/event/100",
        json={"title": "test_title", "start": "2021-07-31", "end": "2021-07-31"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "CATEGORY_NOT_FOUND"}


@pytest.mark.asyncio
async def test_update_calendar_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_calendar_category,
    create_test_calendar,
) -> None:
    access_token = await get_access_token(client)
    response = await client.put(
        "/api/calendar/category/100/event/1000",
        json={"title": "test_title", "start": "2021-07-31", "end": "2021-07-31"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "CALENDAR_NOT_FOUND"}


@pytest.mark.asyncio
async def test_update_calendar_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_calendar_category,
    create_test_calendar,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from event import service

    async def mock_update_calendar(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "update_calendar", mock_update_calendar)

    access_token = await get_access_token(client)
    response = await client.put(
        "/api/calendar/category/100/event/9999",
        json={"title": "test_title", "start": "2021-07-31", "end": "2021-07-31"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 500
    assert response.json() == {"detail": "INTERNAL_SERVER_ERROR"}
