import pytest
from async_asgi_testclient import TestClient
from sqlalchemy import select

from database import fetch_one
from model.reading_room import ReadingRoom
from tests.utils import get_access_token


@pytest.mark.asyncio
async def test_get_reading_room_list(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_reading_room,
) -> None:
    access_token = await get_access_token(client)

    response = await client.get(
        "/api/library",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    response_json = response.json()
    assert response.status_code == 200
    assert response_json.get("data") is not None
    for campus in response_json["data"]:
        assert campus.get("id") is not None
        assert campus.get("name") is not None


@pytest.mark.asyncio
async def test_get_reading_room_list_filter(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_reading_room,
) -> None:
    access_token = await get_access_token(client)

    response = await client.get(
        "/api/library?campus=1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json.get("data") is not None
    for campus in response_json["data"]:
        assert campus.get("id") is not None
        assert campus.get("name") is not None


@pytest.mark.asyncio
async def test_get_reading_room(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_reading_room,
) -> None:
    access_token = await get_access_token(client)

    response = await client.get(
        "/api/library/1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json.get("id") is not None
    assert response_json.get("name") is not None
    assert response_json.get("total") is not None
    assert response_json.get("active") is not None
    assert response_json.get("available") is not None
    assert response_json.get("occupied") is not None


@pytest.mark.asyncio
async def test_get_reading_room_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_reading_room,
) -> None:
    access_token = await get_access_token(client)

    response = await client.get(
        "/api/library/100",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json().get("detail") == "ROOM_NOT_FOUND"


@pytest.mark.asyncio
async def test_create_reading_room(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_reading_room,
) -> None:
    access_token = await get_access_token(client)

    response = await client.post(
        "/api/library",
        json={
            "campusID": 1,
            "id": 100,
            "name": "제1열람실",
            "active": False,
            "reservable": False,
            "total": 100,
            "active_total": 0,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 201

    response_json = response.json()
    assert response_json.get("id") is not None
    assert response_json.get("name") is not None
    assert response_json.get("total") is not None
    assert response_json.get("active") is not None
    assert response_json.get("available") is not None
    assert response_json.get("occupied") is not None
    check_statement = (
        select(ReadingRoom).where(ReadingRoom.id_ == 100)
    )
    query_result = await fetch_one(check_statement)
    assert query_result is not None
    assert query_result.id_ == 100


@pytest.mark.asyncio
async def test_create_reading_room_duplicate_id(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_reading_room,
) -> None:
    access_token = await get_access_token(client)

    response = await client.post(
        "/api/library",
        json={
            "campusID": 1,
            "id": 1,
            "name": "제1열람실",
            "active": False,
            "reservable": False,
            "total": 100,
            "active_total": 0,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 409
    assert response.json().get("detail") == "DUPLICATE_ROOM_ID"


@pytest.mark.asyncio
async def test_create_reading_room_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    monkeypatch: pytest.MonkeyPatch,
):
    from reading_room import service

    async def fake_getter(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "create_reading_room", fake_getter)

    access_token = await get_access_token(client)

    response = await client.post(
        "/api/library",
        json={
            "campusID": 1,
            "id": 1,
            "name": "제1열람실",
            "active": False,
            "reservable": False,
            "total": 100,
            "active_total": 0,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 500
    assert response.json() == {
        "detail": "INTERNAL_SERVER_ERROR",
    }


@pytest.mark.asyncio
async def test_update_reading_room(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_reading_room,
) -> None:
    access_token = await get_access_token(client)

    response = await client.patch(
        "/api/library/1",
        json={
            "isActive": False,
            "isReservable": False,
            "total": 100,
            "active": 50,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json.get("id") is not None
    assert response_json.get("name") is not None
    assert response_json.get("total") is not None
    assert response_json.get("active") is not None
    assert response_json.get("available") is not None
    assert response_json.get("occupied") is not None


@pytest.mark.asyncio
async def test_update_reading_room_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_reading_room,
) -> None:
    access_token = await get_access_token(client)

    response = await client.patch(
        "/api/library/100",
        json={
            "isActive": False,
            "isReservable": False,
            "total": 100,
            "active": 50,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json().get("detail") == "ROOM_NOT_FOUND"


@pytest.mark.asyncio
async def test_update_reading_room_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_reading_room,
    monkeypatch: pytest.MonkeyPatch,
):
    from reading_room import service

    async def fake_getter(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "update_reading_room", fake_getter)

    access_token = await get_access_token(client)

    response = await client.patch(
        "/api/library/1",
        json={
            "isActive": False,
            "isReservable": False,
            "total": 100,
            "active": 50,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 500
    assert response.json() == {
        "detail": "INTERNAL_SERVER_ERROR",
    }


@pytest.mark.asyncio
async def test_delete_reading_room(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_reading_room,
) -> None:
    access_token = await get_access_token(client)

    response = await client.delete(
        "/api/library/1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_reading_room_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_reading_room,
) -> None:
    access_token = await get_access_token(client)

    response = await client.delete(
        "/api/library/100",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json().get("detail") == "ROOM_NOT_FOUND"
