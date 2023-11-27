import pytest
from async_asgi_testclient import TestClient


@pytest.mark.asyncio
async def test_register_user(client: TestClient) -> None:
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
