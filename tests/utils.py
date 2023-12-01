from async_asgi_testclient import TestClient


async def get_access_token(client: TestClient) -> str:
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

    assert access_token is not None
    return access_token
