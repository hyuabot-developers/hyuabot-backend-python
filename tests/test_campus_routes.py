import pytest
from async_asgi_testclient import TestClient

from tests.utils import get_access_token


@pytest.mark.asyncio
async def test_get_campus_list(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_campus,
) -> None:
    access_token = await get_access_token(client)

    response = await client.get(
        "/api/campus",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    response_json = response.json()
    print(response_json)
    assert response.status_code == 200
    assert response_json.get("data") is not None
    for campus in response_json["data"]:
        assert campus.get("id") is not None
        assert campus.get("name") is not None


@pytest.mark.asyncio
async def test_get_campus_list_filter(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_campus,
) -> None:
    access_token = await get_access_token(client)

    response = await client.get(
        "/api/campus?name=test_campus1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json.get("data") is not None
    for campus in response_json["data"]:
        assert campus.get("id") is not None
        assert "test_campus1" in campus.get("name")


@pytest.mark.asyncio
async def test_get_campus(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_campus,
) -> None:
    access_token = await get_access_token(client)

    response = await client.get(
        "/api/campus/1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json.get("id") is not None
    assert response_json.get("name") is not None


@pytest.mark.asyncio
async def test_get_campus_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_campus,
) -> None:
    access_token = await get_access_token(client)

    response = await client.get(
        "/api/campus/100",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json().get("detail") == "CAMPUS_NOT_FOUND"


@pytest.mark.asyncio
async def test_create_campus(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_campus,
) -> None:
    access_token = await get_access_token(client)

    response = await client.post(
        "/api/campus",
        json={
            "id": 100,
            "name": "test_campus100",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 201

    response_json = response.json()
    assert response_json.get("id") is not None
    assert response_json.get("name") is not None


@pytest.mark.asyncio
async def test_create_campus_duplicate_id(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_campus,
) -> None:
    access_token = await get_access_token(client)

    response = await client.post(
        "/api/campus",
        json={
            "id": 1,
            "name": "test_campus1",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 409
    assert response.json().get("detail") == "DUPLICATE_CAMPUS_ID"


@pytest.mark.asyncio
async def test_create_campus_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    monkeypatch: pytest.MonkeyPatch,
):
    from campus import service

    async def fake_getter(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "create_campus", fake_getter)

    access_token = await get_access_token(client)

    response = await client.post(
        "/api/campus",
        json={
            "id": 1,
            "name": "test_campus1",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 500
    assert response.json() == {
        "detail": "INTERNAL_SERVER_ERROR",
    }


@pytest.mark.asyncio
async def test_update_campus(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_campus,
) -> None:
    access_token = await get_access_token(client)

    response = await client.patch(
        "/api/campus/1",
        json={
            "name": "test_campus1_updated",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json.get("id") is not None
    assert response_json.get("name") is not None
    assert response_json.get("name") == "test_campus1_updated"


@pytest.mark.asyncio
async def test_update_campus_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_campus,
) -> None:
    access_token = await get_access_token(client)

    response = await client.patch(
        "/api/campus/100",
        json={
            "name": "test_campus100_updated",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json().get("detail") == "CAMPUS_NOT_FOUND"


@pytest.mark.asyncio
async def test_update_campus_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_campus,
    monkeypatch: pytest.MonkeyPatch,
):
    from campus import service

    async def fake_getter(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "update_campus", fake_getter)

    access_token = await get_access_token(client)

    response = await client.patch(
        "/api/campus/1",
        json={
            "name": "test_campus1",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 500
    assert response.json() == {
        "detail": "INTERNAL_SERVER_ERROR",
    }


@pytest.mark.asyncio
async def test_delete_campus(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_campus,
) -> None:
    access_token = await get_access_token(client)

    response = await client.delete(
        "/api/campus/1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_campus_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_campus,
) -> None:
    access_token = await get_access_token(client)

    response = await client.delete(
        "/api/campus/100",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json().get("detail") == "CAMPUS_NOT_FOUND"
