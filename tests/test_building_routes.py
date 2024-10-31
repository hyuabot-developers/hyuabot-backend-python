import pytest
from async_asgi_testclient import TestClient
from sqlalchemy import select

from database import fetch_one
from model.building import Building, Room
from tests.utils import get_access_token


@pytest.mark.asyncio
async def test_building_list(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_building,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/building",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json["data"]) > 0
    for building in response_json["data"]:
        assert building["id"] is not None
        assert building["name"] is not None
        assert building["campusID"] is not None
        assert building["latitude"] is not None
        assert building["longitude"] is not None
        assert building["url"] is not None


@pytest.mark.asyncio
async def test_building_list_filter_name(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_building,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/building?name=test_building",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json["data"]) > 0
    for building in response_json["data"]:
        assert building["id"] is not None
        assert "test_building" in building["name"]
        assert building["campusID"] is not None
        assert building["latitude"] is not None
        assert building["longitude"] is not None
        assert building["url"] is not None


@pytest.mark.asyncio
async def test_building_list_filter_campus(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_building,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/building?campus=1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json["data"]) > 0
    for building in response_json["data"]:
        assert building["id"] is not None
        assert building["name"] is not None
        assert building["campusID"] == 1
        assert building["latitude"] is not None
        assert building["longitude"] is not None
        assert building["url"] is not None


@pytest.mark.asyncio
async def test_building_list_filter_campus_and_name(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_building,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/building?campus=1&name=test_building",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json["data"]) > 0
    for building in response_json["data"]:
        assert building["id"] is not None
        assert "test_building" in building["name"]
        assert building["campusID"] == 1
        assert building["latitude"] is not None
        assert building["longitude"] is not None
        assert building["url"] is not None


@pytest.mark.asyncio
async def test_create_building(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_building,
):
    access_token = await get_access_token(client)
    response = await client.post(
        "/api/building",
        json={
            "id": "test_id",
            "name": "test_name",
            "campusID": 1,
            "latitude": 37.123456,
            "longitude": 127.123456,
            "url": "https://blog.naver.com/hyerica4473/223122445405",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 201
    response_json = response.json()
    assert response_json["id"] is not None
    assert response_json["name"] is not None
    assert response_json["campusID"] is not None
    assert response_json["latitude"] is not None
    assert response_json["longitude"] is not None
    assert response_json["url"] is not None
    check_statement = (
        select(Building).where(Building.id_ == "test_id")
    )
    query_result = await fetch_one(check_statement)
    assert query_result is not None
    assert query_result.name == "test_name"


@pytest.mark.asyncio
async def test_create_building_with_duplicated_id(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_building,
):
    access_token = await get_access_token(client)
    response = await client.post(
        "/api/building",
        json={
            "id": "1",
            "name": "test_building1",
            "campusID": 1,
            "latitude": 37.123456,
            "longitude": 127.123456,
            "url": "https://blog.naver.com/hyerica4473/223122445405",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_create_building_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_building,
    monkeypatch,
):
    from building import service

    async def mock_create_building(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "create_building", mock_create_building)
    access_token = await get_access_token(client)
    response = await client.post(
        "/api/building",
        json={
            "id": "test_id",
            "name": "test_name",
            "campusID": 1,
            "latitude": 37.123456,
            "longitude": 127.123456,
            "url": "https://blog.naver.com/hyerica4473/223122445405",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 500


@pytest.mark.asyncio
async def test_get_building(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_building,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/building/test_building1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["id"] is not None
    assert response_json["name"] is not None
    assert response_json["campusID"] is not None
    assert response_json["latitude"] is not None
    assert response_json["longitude"] is not None
    assert response_json["url"] is not None


@pytest.mark.asyncio
async def test_get_building_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/building/test_building1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    response_json = response.json()
    assert response_json["detail"] == "BUILDING_NOT_FOUND"


@pytest.mark.asyncio
async def test_patch_building(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_building,
):
    access_token = await get_access_token(client)
    response = await client.patch(
        "/api/building/test_building1",
        json={
            "id": "Y204",
            "latitude": 37.123456,
            "longitude": 127.123456,
            "url": "https://blog.naver.com/hyerica4473/223122445405",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["id"] is not None
    assert response_json["name"] is not None
    assert response_json["campusID"] is not None
    assert response_json["latitude"] is not None
    assert response_json["longitude"] is not None
    assert response_json["url"] is not None


@pytest.mark.asyncio
async def test_patch_building_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
):
    access_token = await get_access_token(client)
    response = await client.patch(
        "/api/building/test_building1",
        json={
            "id": "Y204",
            "latitude": 37.123456,
            "longitude": 127.123456,
            "url": "https://blog.naver.com/hyerica4473/223122445405",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    response_json = response.json()
    assert response_json["detail"] == "BUILDING_NOT_FOUND"


@pytest.mark.asyncio
async def test_patch_building_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_building,
    monkeypatch,
):
    from building import service

    async def mock_update_building(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "update_building", mock_update_building)
    access_token = await get_access_token(client)
    response = await client.patch(
        "/api/building/test_building1",
        json={
            "id": "Y204",
            "latitude": 37.123456,
            "longitude": 127.123456,
            "url": "https://blog.naver.com/hyerica4473/223122445405",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 500
    response_json = response.json()
    assert response_json["detail"] == "INTERNAL_SERVER_ERROR"


@pytest.mark.asyncio
async def test_delete_building(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_building,
):
    access_token = await get_access_token(client)
    response = await client.delete(
        "/api/building/test_building1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_building_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
):
    access_token = await get_access_token(client)
    response = await client.delete(
        "/api/building/test_building1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    response_json = response.json()
    assert response_json["detail"] == "BUILDING_NOT_FOUND"


@pytest.mark.asyncio
async def test_delete_building_has_room(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_room,
):
    access_token = await get_access_token(client)
    response = await client.delete(
        "/api/building/test_building1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 400
    response_json = response.json()
    assert response_json["detail"] == "BUILDING_HAS_ROOM"


@pytest.mark.asyncio
async def test_list_room_in_a_building(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_room,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/building/test_building1/room",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json["data"]) > 0
    for room in response_json["data"]:
        assert room["buildingID"] is not None
        assert room["name"] is not None
        assert room["number"] is not None


@pytest.mark.asyncio
async def test_list_room_in_a_building_filter_name(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_room,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/building/test_building1/room?name=test_room",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json["data"]) > 0
    for room in response_json["data"]:
        assert room["buildingID"] is not None
        assert "test_room" in room["name"]
        assert room["number"] is not None


@pytest.mark.asyncio
async def test_list_room_in_a_building_filter_floor(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_room,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/building/test_building1/room?floor=1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json["data"]) > 0
    for room in response_json["data"]:
        assert room["buildingID"] is not None
        assert room["name"] is not None
        assert room["number"] is not None


@pytest.mark.asyncio
async def test_list_room_in_a_building_filter_number(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_room,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/building/test_building1/room?number=101",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json["data"]) > 0
    for room in response_json["data"]:
        assert room["buildingID"] is not None
        assert room["name"] is not None
        assert room["number"] == "101"


@pytest.mark.asyncio
async def test_create_room_in_a_building(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_building,
):
    access_token = await get_access_token(client)
    response = await client.post(
        "/api/building/test_building1/room",
        json={
            "name": "test_name",
            "number": "101",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 201
    response_json = response.json()
    assert response_json["buildingID"] is not None
    assert response_json["name"] is not None
    assert response_json["number"] is not None
    check_statement = (
        select(Room).where(Room.name == "test_name")
    )
    query_result = await fetch_one(check_statement)
    assert query_result is not None
    assert query_result.number == "101"


@pytest.mark.asyncio
async def test_create_room_in_a_building_with_duplicated_id(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_building,
    create_test_room,
):
    access_token = await get_access_token(client)
    response = await client.post(
        "/api/building/test_building1/room",
        json={
            "name": "test_name",
            "number": "101",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 409
    response_json = response.json()
    assert response_json["detail"] == "DUPLICATE_ROOM_ID"


@pytest.mark.asyncio
async def test_create_room_in_a_building_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
):
    access_token = await get_access_token(client)
    response = await client.post(
        "/api/building/test_building1/room",
        json={
            "name": "test_name",
            "number": "101",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    response_json = response.json()
    assert response_json["detail"] == "BUILDING_NOT_FOUND"


@pytest.mark.asyncio
async def test_create_room_in_a_building_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_building,
    monkeypatch,
):
    from building import service

    async def mock_create_room(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "create_room", mock_create_room)
    access_token = await get_access_token(client)
    response = await client.post(
        "/api/building/test_building1/room",
        json={
            "name": "test_name",
            "number": "101",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 500
    response_json = response.json()
    assert response_json["detail"] == "INTERNAL_SERVER_ERROR"


@pytest.mark.asyncio
async def test_get_room_in_a_building(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_room,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/building/test_building1/room/101",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["buildingID"] is not None
    assert response_json["name"] is not None
    assert response_json["number"] is not None


@pytest.mark.asyncio
async def test_get_room_in_a_building_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_building,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/building/test_building1/room/101",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    response_json = response.json()
    assert response_json["detail"] == "ROOM_NOT_FOUND"


@pytest.mark.asyncio
async def test_patch_room_in_a_building(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_room,
):
    access_token = await get_access_token(client)
    response = await client.patch(
        "/api/building/test_building1/room/101",
        json={
            "name": "test_name",
            "number": "101",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["buildingID"] is not None
    assert response_json["name"] is not None
    assert response_json["number"] is not None


@pytest.mark.asyncio
async def test_patch_room_in_a_building_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_building,
):
    access_token = await get_access_token(client)
    response = await client.patch(
        "/api/building/test_building1/room/101",
        json={
            "name": "test_name",
            "number": "101",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    response_json = response.json()
    assert response_json["detail"] == "ROOM_NOT_FOUND"


@pytest.mark.asyncio
async def test_patch_room_in_a_building_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_room,
    monkeypatch,
):
    from building import service

    async def mock_update_room(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "update_room", mock_update_room)
    access_token = await get_access_token(client)
    response = await client.patch(
        "/api/building/test_building1/room/101",
        json={
            "name": "test_name",
            "number": "101",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 500
    response_json = response.json()
    assert response_json["detail"] == "INTERNAL_SERVER_ERROR"


@pytest.mark.asyncio
async def test_delete_room_in_a_building(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_room,
):
    access_token = await get_access_token(client)
    response = await client.delete(
        "/api/building/test_building1/room/101",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_room_in_a_building_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_building,
):
    access_token = await get_access_token(client)
    response = await client.delete(
        "/api/building/test_building1/room/101",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    response_json = response.json()
    assert response_json["detail"] == "ROOM_NOT_FOUND"
