import pytest
from async_asgi_testclient import TestClient
from sqlalchemy import select

from database import fetch_one
from model.notice import NoticeCategory, Notice
from tests.utils import get_access_token


@pytest.mark.asyncio
async def test_get_notice_category_list(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_notice_category,
) -> None:
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/notice",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("data") is not None
    assert len(response_json["data"]) > 0
    for notice_category in response_json["data"]:
        assert notice_category.get("id") is not None
        assert notice_category.get("name") is not None


@pytest.mark.asyncio
async def test_get_notice_category_list_filter(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_notice_category,
) -> None:
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/notice?name=test_category",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("data") is not None
    assert len(response_json["data"]) > 0
    for notice_category in response_json["data"]:
        assert notice_category.get("id") is not None
        assert "test_category" in notice_category.get("name")


@pytest.mark.asyncio
async def test_create_notice_category(
    client: TestClient,
    clean_db,
    create_test_user,
) -> None:
    access_token = await get_access_token(client)
    response = await client.post(
        "/api/notice",
        json={"name": "test_category"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 201
    response_json = response.json()
    assert response_json.get("id") is not None
    assert response_json.get("name") is not None
    assert response_json["name"] == "test_category"
    check_statement = select(NoticeCategory).where(NoticeCategory.name == "test_category")
    query_result = await fetch_one(check_statement)
    assert query_result is not None
    assert query_result.name == "test_category"


@pytest.mark.asyncio
async def test_create_notice_category_duplicated_name(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_notice_category,
) -> None:
    access_token = await get_access_token(client)
    response = await client.post(
        "/api/notice",
        json={"name": "test_category100"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "DUPLICATE_CATEGORY_NAME"}


@pytest.mark.asyncio
async def test_create_notice_category_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_notice_category,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from notice import service

    async def mock_create_notice_category(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "create_notice_category", mock_create_notice_category)

    access_token = await get_access_token(client)
    response = await client.post(
        "/api/notice",
        json={"name": "test_category"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 500
    assert response.json() == {"detail": "INTERNAL_SERVER_ERROR"}


@pytest.mark.asyncio
async def test_get_notice_category(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_notice_category,
) -> None:
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/notice/100",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("id") == 100
    assert response_json.get("name") == "test_category100"


@pytest.mark.asyncio
async def test_get_notice_category_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_notice_category,
) -> None:
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/notice/1000",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "CATEGORY_NOT_FOUND"}


@pytest.mark.asyncio
async def test_delete_notice_category(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_notice_category,
) -> None:
    access_token = await get_access_token(client)
    response = await client.delete(
        "/api/notice/100",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_notice_category_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_notice_category,
) -> None:
    access_token = await get_access_token(client)
    response = await client.delete(
        "/api/notice/1000",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "CATEGORY_NOT_FOUND"}


@pytest.mark.asyncio
async def test_get_notice_list(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_notice_category,
    create_test_notice,
) -> None:
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/notice/100/notices",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("data") is not None
    assert len(response_json["data"]) > 0
    for notice in response_json["data"]:
        assert notice.get("id") is not None
        assert notice.get("title") is not None
        assert notice.get("userID") is not None
        assert notice.get("expiredAt") is not None
        assert notice.get("language") is not None
        assert notice.get("url") is not None


@pytest.mark.asyncio
async def test_get_notice_list_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_notice_category,
    create_test_notice,
) -> None:
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/notice/1000/notices",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "CATEGORY_NOT_FOUND"}


@pytest.mark.asyncio
async def test_get_notice(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_notice_category,
    create_test_notice,
) -> None:
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/notice/100/notices/9999",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("id") == 9999
    assert response_json.get("title") == "test_title9999"
    assert response_json.get("userID") == "test_id"
    assert response_json.get("expiredAt") is not None
    assert response_json.get("language") in ["korean", "english"]
    assert response_json.get("url") == "test_url"


@pytest.mark.asyncio
async def test_get_notice_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_notice_category,
    create_test_notice,
) -> None:
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/notice/100/notices/100",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "NOTICE_NOT_FOUND"}


@pytest.mark.asyncio
async def test_create_notice(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_notice_category,
) -> None:
    access_token = await get_access_token(client)
    response = await client.post(
        "/api/notice/100/notices",
        json={
            "title": "test_title",
            "url": "test_url",
            "expired": "2021-07-31T00:00:00+09:00",
            "language": "korean",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 201
    response_json = response.json()
    assert response_json.get("id") is not None
    assert response_json.get("title") == "test_title"
    assert response_json.get("userID") == "test_id"
    assert response_json.get("expiredAt") is not None
    assert response_json.get("language") == "korean"
    assert response_json.get("url") == "test_url"
    check_statement = select(Notice).where(Notice.title == "test_title")
    query_result = await fetch_one(check_statement)
    assert query_result is not None
    assert query_result.title == "test_title"


@pytest.mark.asyncio
async def test_create_notice_category_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_notice_category,
) -> None:
    access_token = await get_access_token(client)
    response = await client.post(
        "/api/notice/1000/notices",
        json={
            "title": "test_title",
            "url": "test_url",
            "expired": "2021-07-31T00:00:00+09:00",
            "language": "korean",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "CATEGORY_NOT_FOUND"}


@pytest.mark.asyncio
async def test_create_notice_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_notice_category,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from notice import service

    async def mock_create_notice(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "create_notice", mock_create_notice)

    access_token = await get_access_token(client)
    response = await client.post(
        "/api/notice/100/notices",
        json={
            "title": "test_title",
            "url": "test_url",
            "expired": "2021-07-31T00:00:00+09:00",
            "language": "korean",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 500
    assert response.json() == {"detail": "INTERNAL_SERVER_ERROR"}


@pytest.mark.asyncio
async def test_delete_notice(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_notice_category,
    create_test_notice,
) -> None:
    access_token = await get_access_token(client)
    response = await client.delete(
        "/api/notice/100/notices/100",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_update_notice(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_notice_category,
    create_test_notice,
) -> None:
    access_token = await get_access_token(client)
    response = await client.patch(
        "/api/notice/100/notices/9999",
        json={
            "title": "test_title",
            "url": "test_url",
            "expired": "2021-07-31T00:00:00+09:00",
            "language": "korean",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("id") is not None
    assert response_json.get("title") == "test_title"
    assert response_json.get("userID") == "test_id"
    assert response_json.get("expiredAt") is not None
    assert response_json.get("language") == "korean"
    assert response_json.get("url") == "test_url"


@pytest.mark.asyncio
async def test_update_notice_category_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_notice_category,
    create_test_notice,
) -> None:
    access_token = await get_access_token(client)
    response = await client.patch(
        "/api/notice/1000/notices/100",
        json={"title": "test_title", "url": "test_url"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "CATEGORY_NOT_FOUND"}


@pytest.mark.asyncio
async def test_update_notice_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_notice_category,
    create_test_notice,
) -> None:
    access_token = await get_access_token(client)
    response = await client.patch(
        "/api/notice/100/notices/1000",
        json={"title": "test_title", "url": "test_url"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "NOTICE_NOT_FOUND"}


@pytest.mark.asyncio
async def test_update_notice_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_notice_category,
    create_test_notice,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from notice import service

    async def mock_update_notice(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "update_notice", mock_update_notice)

    access_token = await get_access_token(client)
    response = await client.patch(
        "/api/notice/100/notices/9999",
        json={"title": "test_title", "url": "test_url"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 500
    assert response.json() == {"detail": "INTERNAL_SERVER_ERROR"}
