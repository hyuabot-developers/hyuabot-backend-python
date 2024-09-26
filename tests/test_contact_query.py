import pytest
from async_asgi_testclient import TestClient

from query.router import graphql_schema


@pytest.mark.asyncio
async def test_contact_query(
    client: TestClient,
    clean_db,
    create_test_contact,
    create_test_contact_version,
):
    query = """
        query {
            contact {
                version,
                data {
                    category { id, name }
                    campusID, name, phone
                }
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["contact"], dict)
    contact_data = response.data["contact"]
    assert len(contact_data["data"]) > 0
    for contact in contact_data["data"]:
        assert isinstance(contact, dict)
        assert "category" in contact.keys()
        assert "campusID" in contact.keys()
        assert "name" in contact.keys()
        assert "phone" in contact.keys()
        assert "id" in contact["category"].keys()
        assert "name" in contact["category"].keys()


@pytest.mark.asyncio
async def test_contact_query_with_category_filter(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_contact,
    create_test_contact_version,
):
    query = """
        query {
            contact (categoryId: 100) {
                version,
                data {
                    category { id, name }
                    campusID, name, phone
                }
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["contact"], dict)
    contact_data = response.data["contact"]
    assert len(contact_data["data"]) > 0
    for contact in contact_data["data"]:
        assert isinstance(contact, dict)
        assert "category" in contact.keys()
        assert "campusID" in contact.keys()
        assert "name" in contact.keys()
        assert "phone" in contact.keys()
        assert "id" in contact["category"].keys()
        assert "name" in contact["category"].keys()


@pytest.mark.asyncio
async def test_contact_query_with_campus_filter(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_contact,
    create_test_contact_version,
):
    query = """
        query {
            contact (campusId: 1) {
                version,
                data {
                    category { id, name }
                    campusID, name, phone
                }
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["contact"], dict)
    contact_data = response.data["contact"]
    assert len(contact_data["data"]) > 0
    for contact in contact_data["data"]:
        assert isinstance(contact, dict)
        assert "category" in contact.keys()
        assert "campusID" in contact.keys()
        assert contact["campusID"] == 1
        assert "name" in contact.keys()
        assert "phone" in contact.keys()
        assert "id" in contact["category"].keys()
        assert "name" in contact["category"].keys()


@pytest.mark.asyncio
async def test_contact_query_with_filter_by_title(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_contact,
    create_test_contact_version,
):
    query = """
        query {
            contact (name: "test") {
                version,
                data {
                    category { id, name }
                    campusID, name, phone
                }
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["contact"], dict)
    contact_data = response.data["contact"]
    assert len(contact_data["data"]) > 0
    for contact in contact_data["data"]:
        assert isinstance(contact, dict)
        assert "category" in contact.keys()
        assert "campusID" in contact.keys()
        assert "name" in contact.keys()
        assert "phone" in contact.keys()
        assert "id" in contact["category"].keys()
        assert "name" in contact["category"].keys()
