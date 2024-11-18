from datetime import datetime

import pytest
from async_asgi_testclient import TestClient
from sqlalchemy import select

from database import fetch_one
from model.cafeteria import Cafeteria, Menu
from tests.utils import get_access_token


@pytest.mark.asyncio
async def test_get_cafeteria_list(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_cafeteria,
) -> None:
    access_token = await get_access_token(client)

    response = await client.get(
        "/api/cafeteria",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    response_json = response.json()
    assert response.status_code == 200
    assert response_json.get("data") is not None
    assert len(response_json["data"]) > 0
    for campus in response_json["data"]:
        assert campus.get("id") is not None
        assert campus.get("name") is not None


@pytest.mark.asyncio
async def test_get_cafeteria_list_filter(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_cafeteria,
) -> None:
    access_token = await get_access_token(client)

    response = await client.get(
        "/api/cafeteria?campus=1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json.get("data") is not None
    assert len(response_json["data"]) > 0
    for campus in response_json["data"]:
        assert campus.get("id") is not None
        assert campus.get("name") is not None


@pytest.mark.asyncio
async def test_get_cafeteria(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_cafeteria,
) -> None:
    access_token = await get_access_token(client)

    response = await client.get(
        "/api/cafeteria/1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json.get("id") is not None
    assert response_json.get("name") is not None
    assert response_json.get("campusID") is not None
    assert response_json.get("latitude") is not None
    assert response_json.get("longitude") is not None
    assert response_json.get("runningTime") is not None
    running_time = response_json.get("runningTime")
    assert "breakfast" in running_time.keys()
    assert "lunch" in running_time.keys()
    assert "dinner" in running_time.keys()


@pytest.mark.asyncio
async def test_get_cafeteria_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_cafeteria,
) -> None:
    access_token = await get_access_token(client)

    response = await client.get(
        "/api/cafeteria/100",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    response_json = response.json()
    assert response_json.get("detail") == "CAFETERIA_NOT_FOUND"


@pytest.mark.asyncio
async def test_create_cafeteria(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_campus,
) -> None:
    access_token = await get_access_token(client)

    response = await client.post(
        "/api/cafeteria",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "id": 1,
            "name": "test_cafeteria",
            "campusID": 1,
            "latitude": 89.0,
            "longitude": 89.0,
        },
    )
    assert response.status_code == 201

    response_json = response.json()
    assert response_json.get("id") is not None
    assert response_json.get("name") is not None
    assert response_json.get("campusID") is not None
    assert response_json.get("latitude") is not None
    assert response_json.get("longitude") is not None
    assert response_json.get("runningTime") is not None
    running_time = response_json.get("runningTime")
    assert "breakfast" in running_time.keys()
    assert "lunch" in running_time.keys()
    assert "dinner" in running_time.keys()
    check_statement = (
        select(Cafeteria).where(Cafeteria.id_ == 1)
    )
    query_result = await fetch_one(check_statement)
    assert query_result is not None
    assert query_result.name == "test_cafeteria"


@pytest.mark.asyncio
async def test_create_cafeteria_invalid_campus(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_campus,
) -> None:
    access_token = await get_access_token(client)

    response = await client.post(
        "/api/cafeteria",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "id": 1,
            "name": "test_cafeteria",
            "campusID": 100,
            "latitude": 89.0,
            "longitude": 89.0,
        },
    )
    assert response.status_code == 400
    response_json = response.json()
    assert response_json.get("detail") == "INVALID_CAMPUS_ID"


@pytest.mark.asyncio
async def test_create_cafeteria_duplicate(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_campus,
    create_test_cafeteria,
) -> None:
    access_token = await get_access_token(client)

    response = await client.post(
        "/api/cafeteria",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "id": 1,
            "name": "test_cafeteria",
            "campusID": 1,
            "latitude": 89.0,
            "longitude": 89.0,
        },
    )
    assert response.status_code == 409
    response_json = response.json()
    assert response_json.get("detail") == "DUPLICATE_CAFETERIA_ID"


@pytest.mark.asyncio
async def test_create_cafeteria_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_campus,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from cafeteria import service

    async def mock_create_cafeteria(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "create_cafeteria", mock_create_cafeteria)

    access_token = await get_access_token(client)

    response = await client.post(
        "/api/cafeteria",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "id": 1,
            "name": "test_cafeteria",
            "campusID": 1,
            "latitude": 89.0,
            "longitude": 89.0,
        },
    )
    assert response.status_code == 500
    assert response.json().get("detail") == "INTERNAL_SERVER_ERROR"


@pytest.mark.asyncio
async def test_update_cafeteria(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_campus,
    create_test_cafeteria,
) -> None:
    access_token = await get_access_token(client)

    response = await client.patch(
        "/api/cafeteria/1",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "name": "test_cafeteria",
            "latitude": 89.0,
            "longitude": 89.0,
            "breakfast": "08:00-09:00",
            "lunch": "12:00-13:00",
            "dinner": "18:00-19:00",
        },
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json.get("id") is not None
    assert response_json.get("name") is not None
    assert response_json.get("campusID") is not None
    assert response_json.get("latitude") is not None
    assert response_json.get("longitude") is not None
    assert response_json.get("runningTime") is not None
    running_time = response_json.get("runningTime")
    assert "breakfast" in running_time.keys()
    assert "lunch" in running_time.keys()
    assert "dinner" in running_time.keys()


@pytest.mark.asyncio
async def test_update_cafeteria_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_campus,
    create_test_cafeteria,
) -> None:
    access_token = await get_access_token(client)

    response = await client.patch(
        "/api/cafeteria/100",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "name": "test_cafeteria",
            "latitude": 89.0,
            "longitude": 89.0,
        },
    )
    assert response.status_code == 404
    response_json = response.json()
    assert response_json.get("detail") == "CAFETERIA_NOT_FOUND"


@pytest.mark.asyncio
async def test_update_cafeteria_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_campus,
    create_test_cafeteria,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from cafeteria import service

    async def mock_update_cafeteria(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "update_cafeteria", mock_update_cafeteria)

    access_token = await get_access_token(client)

    response = await client.patch(
        "/api/cafeteria/1",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "name": "test_cafeteria",
            "latitude": 89.0,
            "longitude": 89.0,
        },
    )
    assert response.status_code == 500
    assert response.json().get("detail") == "INTERNAL_SERVER_ERROR"


@pytest.mark.asyncio
async def test_delete_cafeteria(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_campus,
    create_test_cafeteria,
) -> None:
    access_token = await get_access_token(client)

    response = await client.delete(
        "/api/cafeteria/1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_cafeteria_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_campus,
    create_test_cafeteria,
) -> None:
    access_token = await get_access_token(client)

    response = await client.delete(
        "/api/cafeteria/100",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    response_json = response.json()
    assert response_json.get("detail") == "CAFETERIA_NOT_FOUND"


@pytest.mark.asyncio
async def test_get_cafeteria_menu(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_cafeteria_menu,
) -> None:
    access_token = await get_access_token(client)

    response = await client.get(
        "/api/cafeteria/1/menu",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json.get("data") is not None
    assert len(response_json["data"]) > 0
    for menu in response_json["data"]:
        assert menu.get("date") is not None
        assert menu.get("time") is not None
        assert menu.get("menu") is not None
        assert menu.get("price") is not None


@pytest.mark.asyncio
async def test_get_cafeteria_menu_date_filter(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_cafeteria_menu,
) -> None:
    access_token = await get_access_token(client)

    response = await client.get(
        "/api/cafeteria/1/menu?date=2023-12-01",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json.get("data") is not None
    assert len(response_json["data"]) > 0
    for menu in response_json["data"]:
        assert menu.get("date") is not None
        assert menu.get("time") is not None
        assert menu.get("menu") is not None
        assert menu.get("price") is not None


@pytest.mark.asyncio
async def test_get_cafeteria_menu_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_cafeteria_menu,
) -> None:
    access_token = await get_access_token(client)

    response = await client.get(
        "/api/cafeteria/100/menu",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    response_json = response.json()
    assert response_json.get("detail") == "CAFETERIA_NOT_FOUND"


@pytest.mark.asyncio
async def test_get_cafeteria_menu_item(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_cafeteria_menu,
) -> None:
    access_token = await get_access_token(client)

    response = await client.get(
        "/api/cafeteria/1/menu/2023-12-01/조식/test_menu",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json.get("date") is not None
    assert response_json.get("time") is not None
    assert response_json.get("menu") is not None
    assert response_json.get("price") is not None


@pytest.mark.asyncio
async def test_get_cafeteria_menu_item_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_cafeteria_menu,
) -> None:
    access_token = await get_access_token(client)

    response = await client.get(
        "/api/cafeteria/1/menu/2099-12-01/조식/test_menu",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    response_json = response.json()
    assert response_json.get("detail") == "MENU_NOT_FOUND"


@pytest.mark.asyncio
async def test_create_cafeteria_menu(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_cafeteria,
) -> None:
    access_token = await get_access_token(client)

    response = await client.post(
        "/api/cafeteria/1/menu",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "date": "2021-01-01",
            "time": "조식",
            "menu": "test_menu",
            "price": "1000",
        },
    )
    assert response.status_code == 201

    response_json = response.json()
    assert response_json.get("date") is not None
    assert response_json.get("time") is not None
    assert response_json.get("menu") is not None
    assert response_json.get("price") is not None
    check_statement = (
        select(Menu).where(Menu.restaurant_id == 1)
    )
    query_result = await fetch_one(check_statement)
    assert query_result is not None
    assert query_result.feed_date == datetime.strptime(
        "2021-01-01",
        "%Y-%m-%d"
    ).date()


@pytest.mark.asyncio
async def test_create_cafeteria_menu_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_cafeteria,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from cafeteria import service

    async def mock_create_menu(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "create_menu", mock_create_menu)

    access_token = await get_access_token(client)

    response = await client.post(
        "/api/cafeteria/1/menu",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "date": "2021-01-01",
            "time": "조식",
            "menu": "test_menu",
            "price": "1000",
        },
    )
    assert response.status_code == 500
    assert response.json().get("detail") == "INTERNAL_SERVER_ERROR"


@pytest.mark.asyncio
async def test_create_cafeteria_menu_invalid_cafeteria_id(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_cafeteria,
) -> None:
    access_token = await get_access_token(client)

    response = await client.post(
        "/api/cafeteria/100/menu",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "date": "2021-01-01",
            "time": "조식",
            "menu": "test_menu",
            "price": "1000",
        },
    )
    assert response.status_code == 404
    response_json = response.json()
    assert response_json.get("detail") == "CAFETERIA_NOT_FOUND"


@pytest.mark.asyncio
async def test_create_cafeteria_menu_duplicate(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_cafeteria,
    create_test_cafeteria_menu,
) -> None:
    access_token = await get_access_token(client)

    response = await client.post(
        "/api/cafeteria/1/menu",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "date": "2023-12-01",
            "time": "조식",
            "menu": "test_menu",
            "price": "1000",
        },
    )
    assert response.status_code == 409
    response_json = response.json()
    assert response_json.get("detail") == "DUPLICATE_MENU_ID"


@pytest.mark.asyncio
async def test_update_cafeteria_menu(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_cafeteria_menu,
) -> None:
    access_token = await get_access_token(client)

    response = await client.patch(
        "/api/cafeteria/1/menu/2023-12-01/조식/test_menu",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "price": "1000",
        },
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json.get("date") is not None
    assert response_json.get("time") is not None
    assert response_json.get("menu") is not None
    assert response_json.get("price") == "1000"


@pytest.mark.asyncio
async def test_update_cafeteria_menu_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_cafeteria_menu,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from cafeteria import service

    async def mock_update_menu(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "update_menu", mock_update_menu)

    access_token = await get_access_token(client)

    response = await client.patch(
        "/api/cafeteria/1/menu/2023-12-01/조식/test_menu",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "price": "1000",
        },
    )
    assert response.status_code == 500
    assert response.json().get("detail") == "INTERNAL_SERVER_ERROR"


@pytest.mark.asyncio
async def test_update_cafeteria_menu_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_cafeteria_menu,
) -> None:
    access_token = await get_access_token(client)

    response = await client.patch(
        "/api/cafeteria/1/menu/2099-12-01/조식/test_menu",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "price": "1000",
        },
    )
    assert response.status_code == 404
    response_json = response.json()
    assert response_json.get("detail") == "MENU_NOT_FOUND"


@pytest.mark.asyncio
async def test_delete_cafeteria_menu(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_cafeteria_menu,
) -> None:
    access_token = await get_access_token(client)

    response = await client.delete(
        "/api/cafeteria/1/menu/2023-12-01/조식/test_menu",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_cafeteria_menu_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_cafeteria_menu,
) -> None:
    access_token = await get_access_token(client)

    response = await client.delete(
        "/api/cafeteria/1/menu/2099-12-01/조식/test_menu",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    response_json = response.json()
    assert response_json.get("detail") == "MENU_NOT_FOUND"
