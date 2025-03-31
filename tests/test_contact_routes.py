import pytest
from async_asgi_testclient import TestClient
from sqlalchemy import select

from database import fetch_one
from tests.utils import get_access_token
from model.contact import PhoneBookCategory, PhoneBook


@pytest.mark.asyncio
async def test_get_contact_category_list(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_contact_category,
) -> None:
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/contact",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("data") is not None
    assert len(response_json["data"]) > 0
    for contact_category in response_json["data"]:
        assert contact_category.get("id") is not None
        assert contact_category.get("name") is not None


@pytest.mark.asyncio
async def test_get_contact_category_list_filter(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_contact_category,
) -> None:
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/contact?name=test_category",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("data") is not None
    assert len(response_json["data"]) > 0
    for contact_category in response_json["data"]:
        assert contact_category.get("id") is not None
        assert "test_category" in contact_category.get("name")


@pytest.mark.asyncio
async def test_create_contact_category(
    client: TestClient,
    clean_db,
    create_test_user,
) -> None:
    access_token = await get_access_token(client)
    response = await client.post(
        "/api/contact",
        json={"name": "test_category"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 201
    response_json = response.json()
    assert response_json.get("id") is not None
    assert response_json.get("name") is not None
    assert response_json["name"] == "test_category"
    check_statement = (
        select(PhoneBookCategory).where(PhoneBookCategory.name == "test_category")
    )
    query_result = await fetch_one(check_statement)
    assert query_result is not None
    assert query_result.name == "test_category"


@pytest.mark.asyncio
async def test_create_contact_category_duplicated_name(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_contact_category,
) -> None:
    access_token = await get_access_token(client)
    response = await client.post(
        "/api/contact",
        json={"name": "test_category100"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "DUPLICATE_CATEGORY_NAME"}


@pytest.mark.asyncio
async def test_create_contact_category_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_contact_category,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from contact import service

    async def mock_create_contact_category(*args, **kwargs):
        return None

    monkeypatch.setattr(
        service, "create_contact_category", mock_create_contact_category,
    )

    access_token = await get_access_token(client)
    response = await client.post(
        "/api/contact",
        json={"name": "test_category"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 500
    assert response.json() == {"detail": "INTERNAL_SERVER_ERROR"}


@pytest.mark.asyncio
async def test_get_contact_category(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_contact_category,
) -> None:
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/contact/category/100",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("id") == 100
    assert response_json.get("name") == "test_category100"


@pytest.mark.asyncio
async def test_get_contact_category_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_contact_category,
) -> None:
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/contact/category/1000",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "CATEGORY_NOT_FOUND"}


@pytest.mark.asyncio
async def test_delete_contact_category(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_contact_category,
) -> None:
    access_token = await get_access_token(client)
    response = await client.delete(
        "/api/contact/category/100",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_contact_category_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_contact_category,
) -> None:
    access_token = await get_access_token(client)
    response = await client.delete(
        "/api/contact/category/1000",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "CATEGORY_NOT_FOUND"}


@pytest.mark.asyncio
async def test_get_contact_list(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_contact_category,
    create_test_contact,
) -> None:
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/contact/category/100/contacts",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("data") is not None
    assert len(response_json["data"]) > 0
    for contact in response_json["data"]:
        assert contact.get("id") is not None
        assert contact.get("campusID") is not None
        assert contact.get("name") is not None
        assert contact.get("phone") is not None


@pytest.mark.asyncio
async def test_get_contact_list_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_contact_category,
    create_test_contact,
) -> None:
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/contact/category/1000/contacts",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "CATEGORY_NOT_FOUND"}


@pytest.mark.asyncio
async def test_get_contact(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_contact_category,
    create_test_contact,
) -> None:
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/contact/category/100/contacts/9999",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("id") == 9999
    assert response_json.get("campusID") is not None
    assert response_json.get("name") is not None
    assert response_json.get("phone") is not None


@pytest.mark.asyncio
async def test_get_contact_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_contact_category,
    create_test_contact,
) -> None:
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/contact/category/100/contacts/100",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "CONTACT_NOT_FOUND"}


@pytest.mark.asyncio
async def test_create_contact(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_contact_category,
) -> None:
    access_token = await get_access_token(client)
    response = await client.post(
        "/api/contact/category/100/contacts",
        json={
            "name": "test_name",
            "phone": "test_phone",
            "campusID": 1,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 201
    response_json = response.json()
    assert response_json.get("id") is not None
    assert response_json.get("campusID") == 1
    assert response_json.get("name") == "test_name"
    assert response_json.get("phone") == "test_phone"
    check_statement = select(PhoneBook).where(PhoneBook.name == "test_name")
    query_result = await fetch_one(check_statement)
    assert query_result is not None
    assert query_result.name == "test_name"


@pytest.mark.asyncio
async def test_create_contact_category_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_contact_category,
) -> None:
    access_token = await get_access_token(client)
    response = await client.post(
        "/api/contact/category/1000/contacts",
        json={
            "name": "test_name",
            "phone": "test_phone",
            "campusID": 1,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "CATEGORY_NOT_FOUND"}


@pytest.mark.asyncio
async def test_create_contact_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_contact_category,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from contact import service

    async def mock_create_contact(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "create_contact", mock_create_contact)

    access_token = await get_access_token(client)
    response = await client.post(
        "/api/contact/category/100/contacts",
        json={
            "name": "test_name",
            "phone": "test_phone",
            "campusID": 1,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 500
    assert response.json() == {"detail": "INTERNAL_SERVER_ERROR"}


@pytest.mark.asyncio
async def test_delete_contact(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_contact_category,
    create_test_contact,
) -> None:
    access_token = await get_access_token(client)
    response = await client.delete(
        "/api/contact/category/100/contacts/100",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_update_contact(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_contact_category,
    create_test_contact,
) -> None:
    access_token = await get_access_token(client)
    response = await client.put(
        "/api/contact/category/100/contacts/9999",
        json={
            "name": "test_name",
            "phone": "test_phone",
            "campusID": 1,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("id") is not None
    assert response_json.get("campusID") == 1
    assert response_json.get("name") == "test_name"
    assert response_json.get("phone") == "test_phone"


@pytest.mark.asyncio
async def test_update_contact_category_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_contact_category,
    create_test_contact,
) -> None:
    access_token = await get_access_token(client)
    response = await client.put(
        "/api/contact/category/1000/contacts/100",
        json={
            "name": "test_name",
            "phone": "test_phone",
            "campusID": 1,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "CATEGORY_NOT_FOUND"}


@pytest.mark.asyncio
async def test_update_contact_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_contact_category,
    create_test_contact,
) -> None:
    access_token = await get_access_token(client)
    response = await client.put(
        "/api/contact/category/100/contacts/1000",
        json={
            "name": "test_name",
            "phone": "test_phone",
            "campusID": 1,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "CONTACT_NOT_FOUND"}


@pytest.mark.asyncio
async def test_update_contact_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_contact_category,
    create_test_contact,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from contact import service

    async def mock_update_contact(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "update_contact", mock_update_contact)

    access_token = await get_access_token(client)
    response = await client.put(
        "/api/contact/category/100/contacts/9999",
        json={
            "name": "test_name",
            "phone": "test_phone",
            "campusID": 1,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 500
    assert response.json() == {"detail": "INTERNAL_SERVER_ERROR"}


@pytest.mark.asyncio
async def test_get_contact_list_all(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_contact_category,
    create_test_contact,
) -> None:
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/contact/contacts",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("data") is not None
    assert len(response_json["data"]) > 0
    for contact in response_json["data"]:
        assert contact.get("id") is not None
        assert contact.get("campusID") is not None
        assert contact.get("categoryID") is not None
        assert contact.get("name") is not None
        assert contact.get("phone") is not None


@pytest.mark.asyncio
async def test_get_contact_list_all_filter(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_contact_category,
    create_test_contact,
) -> None:
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/contact/contacts?campusID=1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("data") is not None
    assert len(response_json["data"]) > 0
    for contact in response_json["data"]:
        assert contact.get("id") is not None
        assert contact.get("campusID") == 1
        assert contact.get("categoryID") is not None
        assert contact.get("name") is not None
        assert contact.get("phone") is not None
