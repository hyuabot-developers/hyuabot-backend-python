import pytest
from async_asgi_testclient import TestClient


@pytest.mark.asyncio
async def test_register_user(
    client: TestClient,
    clean_db,
) -> None:
    response = await client.post(
        "/api/auth/users",
        json={
            "username": "test_id",
            "password": "test_password",
            "nickname": "test_name",
            "email": "test@gmail.com",
            "phone": "test_phone",
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        "username": "test_id",
        "nickname": "test_name",
        "email": "test@gmail.com",
        "phone": "test_phone",
        "active": False,
    }


@pytest.mark.asyncio
async def test_register_username_taken(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    clean_db,
) -> None:
    from user.dependancies import service

    async def fake_getter(*args, **kwargs):
        return True

    monkeypatch.setattr(service, "get_user_by_id", fake_getter)
    response = await client.post(
        "/api/auth/users",
        json={
            "username": "test_id",
            "password": "test_password",
            "nickname": "test_name",
            "email": "test@gmail.com",
            "phone": "test_phone",
        },
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "EMAIL_ALREADY_EXISTS",
    }


@pytest.mark.asyncio
async def test_register_fail_to_create_user(
    client: TestClient,
    clean_db,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from user.dependancies import service

    async def fake_getter(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "create_user", fake_getter)
    response = await client.post(
        "/api/auth/users",
        json={
            "username": "test_id",
            "password": "test_password",
            "nickname": "test_name",
            "email": "test@gmail.com",
            "phone": "test_phone",
        },
    )
    assert response.status_code == 500
    assert response.json() == {
        "detail": "INTERNAL_SERVER_ERROR",
    }


@pytest.mark.asyncio
async def test_auth_user(
    client: TestClient,
    clean_db,
    create_test_user,
) -> None:
    response = await client.post(
        "/api/auth/users/token",
        form={
            "username": "test_id",
            "password": "test_password",
        },
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json.get("access_token") is not None
    assert response_json.get("refresh_token") is not None


@pytest.mark.asyncio
async def test_auth_user_invalid_user(
    client: TestClient,
    clean_db,
) -> None:
    response = await client.post(
        "/api/auth/users/token",
        form={
            "username": "test_id",
            "password": "test_password",
        },
    )
    assert response.status_code == 401
    assert response.json() == {
        "detail": "INVALID_CREDENTIALS",
    }


@pytest.mark.asyncio
async def test_auth_user_invalid_password(
    client: TestClient,
    clean_db,
    create_test_user,
) -> None:
    response = await client.post(
        "/api/auth/users/token",
        form={
            "username": "test_id",
            "password": "invalid_password",
        },
    )
    assert response.status_code == 401
    assert response.json() == {
        "detail": "INVALID_CREDENTIALS",
    }


@pytest.mark.asyncio
async def test_refresh_access_token(
    client: TestClient,
    clean_db,
    create_test_user,
) -> None:
    response = await client.post(
        "/api/auth/users/token",
        form={
            "username": "test_id",
            "password": "test_password",
        },
    )
    assert response.status_code == 200

    response_json = response.json()
    refresh_token = response_json.get("refresh_token")

    response = await client.put(
        "/api/auth/users/token",
        cookies={
            "refresh_token": refresh_token,
        },
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("access_token") is not None
    assert response_json.get("refresh_token") is not None


@pytest.mark.asyncio
async def test_refresh_access_token_invalid_refresh_token(
    client: TestClient,
    clean_db,
) -> None:
    response = await client.put(
        "/api/auth/users/token",
        cookies={
            "refresh_token": "refresh_token",
        },
    )
    assert response.status_code == 401
    assert response.json() == {
        "detail": "INVALID_REFRESH_TOKEN",
    }


@pytest.mark.asyncio
async def test_refresh_access_token_invalid_user(
    client: TestClient,
    clean_db,
    create_test_user,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from user import service

    async def fake_getter(*args, **kwargs):
        return None

    response = await client.post(
        "/api/auth/users/token",
        form={
            "username": "test_id",
            "password": "test_password",
        },
    )
    assert response.status_code == 200

    response_json = response.json()
    refresh_token = response_json.get("refresh_token")

    monkeypatch.setattr(service, "get_active_user_by_id", fake_getter)
    response = await client.put(
        "/api/auth/users/token",
        cookies={
            "refresh_token": refresh_token,
        },
    )
    assert response.status_code == 401
    assert response.json() == {
        "detail": "INVALID_REFRESH_TOKEN",
    }


@pytest.mark.asyncio
async def test_refresh_access_token_expired_refresh_token(
    client: TestClient,
    clean_db,
    create_test_user,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from user import dependancies

    monkeypatch.setattr(dependancies, "_validate_refresh_token_user", lambda x: False)

    response = await client.post(
        "/api/auth/users/token",
        form={
            "username": "test_id",
            "password": "test_password",
        },
    )
    assert response.status_code == 200

    response_json = response.json()
    refresh_token = response_json.get("refresh_token")
    response = await client.put(
        "/api/auth/users/token",
        cookies={
            "refresh_token": refresh_token,
        },
    )
    assert response.status_code == 401
    assert response.json() == {
        "detail": "INVALID_REFRESH_TOKEN",
    }


@pytest.mark.asyncio
async def test_get_my_info(
    client: TestClient,
    clean_db,
    create_test_user,
) -> None:
    response = await client.post(
        "/api/auth/users/token",
        form={
            "username": "test_id",
            "password": "test_password",
        },
    )
    assert response.status_code == 200

    response_json = response.json()
    access_token = response_json.get("access_token")

    response = await client.get(
        "/api/auth/users/me",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "username": "test_id",
        "nickname": "test_name",
        "email": "test@gmail.com",
        "phone": "test_phone",
        "active": True,
    }


@pytest.mark.asyncio
async def test_get_my_info_inactive_user(
    client: TestClient,
    clean_db,
    create_test_user,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from user import service

    async def fake_getter(*args, **kwargs):
        return None

    response = await client.post(
        "/api/auth/users/token",
        form={
            "username": "test_id",
            "password": "test_password",
        },
    )
    assert response.status_code == 200

    response_json = response.json()
    access_token = response_json.get("access_token")

    monkeypatch.setattr(service, "get_active_user_by_id", fake_getter)
    response = await client.get(
        "/api/auth/users/me",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 401
    assert response.json() == {
        "detail": "INVALID_CREDENTIALS",
    }


@pytest.mark.asyncio
async def test_get_my_info_invalid_access_token(
    client: TestClient,
    clean_db,
    create_test_user,
) -> None:
    response = await client.get(
        "/api/auth/users/me",
        headers={
            "Authorization": "Bearer ",
        },
    )
    assert response.status_code == 401
    assert response.json() == {
        "detail": "INVALID_ACCESS_TOKEN",
    }


@pytest.mark.asyncio
async def test_get_my_info_empty_access_token(
    client: TestClient,
    clean_db,
    create_test_user,
) -> None:
    response = await client.get(
        "/api/auth/users/me",
    )
    assert response.status_code == 401
    assert response.json() == {
        "detail": "INVALID_ACCESS_TOKEN",
    }


@pytest.mark.asyncio
async def test_logout(
    client: TestClient,
    clean_db,
    create_test_user,
) -> None:
    response = await client.post(
        "/api/auth/users/token",
        form={
            "username": "test_id",
            "password": "test_password",
        },
    )
    assert response.status_code == 200

    response_json = response.json()
    refresh_token = response_json.get("refresh_token")

    response = await client.delete(
        "/api/auth/users/token",
        cookies={
            "refresh_token": refresh_token,
        },
    )
    assert response.status_code == 200
    assert response.cookies.get("refresh_token") is None
