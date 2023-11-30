import pytest
from async_asgi_testclient import TestClient

from tests.utils import get_access_token


@pytest.mark.asyncio
async def test_get_station_list(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_subway_station_name,
) -> None:
    access_token = await get_access_token(client)

    response = await client.get(
        "/api/subway/station/name",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json.get("data") is not None
    for item in response_json.get("data"):
        assert item.get("name") is not None


@pytest.mark.asyncio
async def test_get_station_list_filter_by_name(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_subway_station_name,
) -> None:
    access_token = await get_access_token(client)

    response = await client.get(
        "/api/subway/station/name?name=name2",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json.get("data") is not None
    assert len(response_json.get("data")) == 1
    assert response_json.get("data")[0].get("name") == "test_station_name2"


@pytest.mark.asyncio
async def test_create_station_name(
    client: TestClient,
    clean_db,
    create_test_user,
) -> None:
    access_token = await get_access_token(client)

    response = await client.post(
        "/api/subway/station/name",
        json={
            "name": "test_station_name",
        },
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 201

    response_json = response.json()
    assert response_json.get("name") == "test_station_name"


@pytest.mark.asyncio
async def test_create_station_name_already_exist(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_subway_station_name,
) -> None:
    access_token = await get_access_token(client)

    response = await client.post(
        "/api/subway/station/name",
        json={
            "name": "test_station_name1",
        },
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 409
    assert response.json() == {
        "detail": "DUPLICATE_STATION_NAME",
    }


@pytest.mark.asyncio
async def test_create_station_name_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    monkeypatch: pytest.MonkeyPatch,
):
    from subway import service

    async def fake_getter(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "create_station_name", fake_getter)

    access_token = await get_access_token(client)

    response = await client.post(
        "/api/subway/station/name",
        json={
            "name": "test_station_name",
        },
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 500
    assert response.json() == {
        "detail": "INTERNAL_SERVER_ERROR",
    }


@pytest.mark.asyncio
async def test_get_station_name(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_subway_station_name,
) -> None:
    access_token = await get_access_token(client)

    response = await client.get(
        "/api/subway/station/name/test_station_name1",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json.get("name") == "test_station_name1"


@pytest.mark.asyncio
async def test_get_station_name_not_exist(
    client: TestClient,
    clean_db,
    create_test_user,
) -> None:
    access_token = await get_access_token(client)

    response = await client.get(
        "/api/subway/station/name/test_station_name1",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "STATION_NAME_NOT_FOUND",
    }


@pytest.mark.asyncio
async def test_delete_station_name(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_subway_station_name,
) -> None:
    access_token = await get_access_token(client)

    response = await client.delete(
        "/api/subway/station/name/test_station_name1",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_station_name_not_exist(
    client: TestClient,
    clean_db,
    create_test_user,
) -> None:
    access_token = await get_access_token(client)

    response = await client.delete(
        "/api/subway/station/name/test_station_name1",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "STATION_NAME_NOT_FOUND",
    }


@pytest.mark.asyncio
async def test_get_route_list(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_subway_route,
) -> None:
    access_token = await get_access_token(client)

    response = await client.get(
        "/api/subway/route",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json.get("data") is not None
    for item in response_json.get("data"):
        assert item.get("id") is not None
        assert item.get("name") is not None


@pytest.mark.asyncio
async def test_get_route_list_filter_by_name(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_subway_route,
) -> None:
    access_token = await get_access_token(client)

    response = await client.get(
        "/api/subway/route?name=test_route",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json.get("data") is not None
    assert len(response_json.get("data")) == 1
    assert response_json.get("data")[0].get("id") == 1001
    assert response_json.get("data")[0].get("name") == "test_route"


@pytest.mark.asyncio
async def test_create_route(
    client: TestClient,
    clean_db,
    create_test_user,
) -> None:
    access_token = await get_access_token(client)

    response = await client.post(
        "/api/subway/route",
        json={
            "id": 1001,
            "name": "test_route",
        },
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 201

    response_json = response.json()
    assert response_json.get("id") == 1001
    assert response_json.get("name") == "test_route"


@pytest.mark.asyncio
async def test_create_route_already_exist(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_subway_route,
) -> None:
    access_token = await get_access_token(client)

    response = await client.post(
        "/api/subway/route",
        json={
            "id": 1001,
            "name": "test_route",
        },
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 409
    assert response.json() == {
        "detail": "DUPLICATE_ROUTE_ID",
    }


@pytest.mark.asyncio
async def test_create_route_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    monkeypatch: pytest.MonkeyPatch,
):
    from subway import service

    async def fake_getter(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "create_route", fake_getter)

    access_token = await get_access_token(client)

    response = await client.post(
        "/api/subway/route",
        json={
            "id": 1001,
            "name": "test_route",
        },
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 500
    assert response.json() == {
        "detail": "INTERNAL_SERVER_ERROR",
    }


@pytest.mark.asyncio
async def test_get_route(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_subway_route,
) -> None:
    access_token = await get_access_token(client)

    response = await client.get(
        "/api/subway/route/1001",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json.get("id") == 1001
    assert response_json.get("name") == "test_route"


@pytest.mark.asyncio
async def test_get_route_not_exist(
    client: TestClient,
    clean_db,
    create_test_user,
) -> None:
    access_token = await get_access_token(client)

    response = await client.get(
        "/api/subway/route/1001",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "ROUTE_NOT_FOUND",
    }


@pytest.mark.asyncio
async def test_update_route(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_subway_route,
) -> None:
    access_token = await get_access_token(client)

    response = await client.patch(
        "/api/subway/route/1001",
        json={
            "name": "test_route2",
        },
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_route_not_exist(
    client: TestClient,
    clean_db,
    create_test_user,
) -> None:
    access_token = await get_access_token(client)

    response = await client.patch(
        "/api/subway/route/1001",
        json={
            "name": "test_route2",
        },
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "ROUTE_NOT_FOUND",
    }


@pytest.mark.asyncio
async def test_delete_route(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_subway_route,
) -> None:
    access_token = await get_access_token(client)

    response = await client.delete(
        "/api/subway/route/1001",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_route_not_exist(
    client: TestClient,
    clean_db,
    create_test_user,
) -> None:
    access_token = await get_access_token(client)

    response = await client.delete(
        "/api/subway/route/1001",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "ROUTE_NOT_FOUND",
    }


@pytest.mark.asyncio
async def test_get_route_station_list(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_subway_route_station,
) -> None:
    access_token = await get_access_token(client)

    response = await client.get(
        "/api/subway/station",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json.get("data") is not None
    for item in response_json.get("data"):
        assert item.get("id") is not None
        assert item.get("name") is not None
        assert item.get("routeID") is not None
        assert item.get("sequence") is not None
        assert item.get("cumulativeTime") is not None


@pytest.mark.asyncio
async def test_get_route_station_list_filter_by_route(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_subway_route_station,
) -> None:
    access_token = await get_access_token(client)

    response = await client.get(
        "/api/subway/station?route=1001",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 200
    assert len(response.json().get("data")) == 9
    for item in response.json().get("data"):
        assert item.get("routeID") == 1001


@pytest.mark.asyncio
async def test_get_route_station(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_subway_route_station,
) -> None:
    access_token = await get_access_token(client)

    response = await client.get(
        "/api/subway/station/K001",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json.get("id") == "K001"
    assert response_json.get("name") == "test_station_name1"
    assert response_json.get("routeID") == 1001
    assert response_json.get("sequence") == 1
    assert response_json.get("cumulativeTime") == "00:01:00"


@pytest.mark.asyncio
async def test_get_route_station_not_exist(
    client: TestClient,
    clean_db,
    create_test_user,
) -> None:
    access_token = await get_access_token(client)

    response = await client.get(
        "/api/subway/station/K001",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "STATION_NOT_FOUND",
    }


@pytest.mark.asyncio
async def test_create_route_station(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_subway_route,
    create_test_subway_station_name,
) -> None:
    access_token = await get_access_token(client)

    response = await client.post(
        "/api/subway/station",
        json={
            "id": "K001",
            "name": "test_station_name1",
            "routeID": 1001,
            "sequence": 1,
            "cumulativeTime": "00:01:00",
        },
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 201

    response_json = response.json()
    assert response_json.get("id") == "K001"
    assert response_json.get("name") == "test_station_name1"
    assert response_json.get("routeID") == 1001
    assert response_json.get("sequence") == 1
    assert response_json.get("cumulativeTime") == "00:01:00"


@pytest.mark.asyncio
async def test_create_route_station_already_exist(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_subway_route_station,
) -> None:
    access_token = await get_access_token(client)

    response = await client.post(
        "/api/subway/station",
        json={
            "id": "K001",
            "name": "test_station_name1",
            "routeID": 1001,
            "sequence": 1,
            "cumulativeTime": "00:01:00",
        },
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 409
    assert response.json() == {
        "detail": "DUPLICATE_STATION_ID",
    }


@pytest.mark.asyncio
async def test_create_route_station_invalid_route(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_subway_route,
    create_test_subway_station_name,
    monkeypatch: pytest.MonkeyPatch,
):
    from subway import service

    async def fake_getter(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "create_route_station", fake_getter)

    access_token = await get_access_token(client)

    response = await client.post(
        "/api/subway/station",
        json={
            "id": "K001",
            "name": "test_station_name1",
            "routeID": 1002,
            "sequence": 1,
            "cumulativeTime": "00:01:00",
        },
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "ROUTE_NOT_FOUND",
    }


@pytest.mark.asyncio
async def test_create_route_station_invalid_name(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_subway_route,
    create_test_subway_station_name,
    monkeypatch: pytest.MonkeyPatch,
):
    from subway import service

    async def fake_getter(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "create_route_station", fake_getter)

    access_token = await get_access_token(client)

    response = await client.post(
        "/api/subway/station",
        json={
            "id": "K001",
            "name": "test_station_name10",
            "routeID": 1001,
            "sequence": 1,
            "cumulativeTime": "00:01:00",
        },
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "STATION_NAME_NOT_FOUND",
    }


@pytest.mark.asyncio
async def test_create_route_station_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_subway_route,
    create_test_subway_station_name,
    monkeypatch: pytest.MonkeyPatch,
):
    from subway import service

    async def fake_getter(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "create_route_station", fake_getter)

    access_token = await get_access_token(client)

    response = await client.post(
        "/api/subway/station",
        json={
            "id": "K001",
            "name": "test_station_name1",
            "routeID": 1001,
            "sequence": 1,
            "cumulativeTime": "00:01:00",
        },
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 500
    assert response.json() == {
        "detail": "INTERNAL_SERVER_ERROR",
    }


@pytest.mark.asyncio
async def test_update_route_station(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_subway_route_station,
    create_test_subway_station_name,
) -> None:
    access_token = await get_access_token(client)

    response = await client.patch(
        "/api/subway/station/K001",
        json={
            "id": "K001",
            "name": "test_station_name1",
            "routeID": 1001,
            "sequence": 1,
            "cumulativeTime": "00:01:00",
        },
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_route_station_not_exist(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_subway_route_station,
    create_test_subway_station_name,
) -> None:
    access_token = await get_access_token(client)

    response = await client.patch(
        "/api/subway/station/K001",
        json={
            "id": "K001",
            "routeID": 1001,
            "sequence": 1,
            "cumulativeTime": "00:01:00",
        },
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_route_station(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_subway_route_station,
    create_test_subway_station_name,
) -> None:
    access_token = await get_access_token(client)

    response = await client.delete(
        "/api/subway/station/K001",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_route_station_not_exist(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_subway_route_station,
    create_test_subway_station_name,
) -> None:
    access_token = await get_access_token(client)

    response = await client.delete(
        "/api/subway/station/K001",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_get_subway_timetable_list(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_subway_timetable,
) -> None:
    access_token = await get_access_token(client)

    response = await client.get(
        "/api/subway/station/K001/timetable",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 200
    assert len(response.json().get("data")) > 0
    for item in response.json().get("data"):
        assert item.get("stationID") is not None
        assert item.get("startStationID") is not None
        assert item.get("terminalStationID") is not None
        assert item.get("departureTime") is not None
        assert item.get("weekday") is not None
        assert item.get("heading") is not None


@pytest.mark.asyncio
async def test_create_subway_timetable(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_subway_route_station,
) -> None:
    access_token = await get_access_token(client)

    response = await client.post(
        "/api/subway/station/K001/timetable",
        json={
            "startStationID": "K001",
            "terminalStationID": "K009",
            "departureTime": "00:00:00",
            "weekday": "weekdays",
            "heading": "true",
        },
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 201

    response_json = response.json()
    assert response_json.get("stationID") is not None
    assert response_json.get("startStationID") is not None
    assert response_json.get("terminalStationID") is not None
    assert response_json.get("departureTime") is not None
    assert response_json.get("weekday") is not None
    assert response_json.get("heading") is not None


@pytest.mark.asyncio
async def test_create_subway_timetable_already_exist(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_subway_timetable,
) -> None:
    access_token = await get_access_token(client)

    response = await client.post(
        "/api/subway/station/K001/timetable",
        json={
            "startStationID": "K001",
            "terminalStationID": "K009",
            "departureTime": "00:01:00",
            "weekday": "weekdays",
            "heading": "up",
        },
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 409
    assert response.json() == {
        "detail": "DUPLICATE_TIMETABLE",
    }


@pytest.mark.asyncio
async def test_create_subway_timetable_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_subway_route_station,
    monkeypatch: pytest.MonkeyPatch,
):
    from subway import service

    async def fake_getter(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "create_timetable", fake_getter)

    access_token = await get_access_token(client)

    response = await client.post(
        "/api/subway/station/K001/timetable",
        json={
            "startStationID": "K001",
            "terminalStationID": "K009",
            "departureTime": "00:00:00",
            "weekday": "weekdays",
            "heading": "true",
        },
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 500
    assert response.json() == {
        "detail": "INTERNAL_SERVER_ERROR",
    }


@pytest.mark.asyncio
async def test_get_subway_timetable(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_subway_timetable,
) -> None:
    access_token = await get_access_token(client)

    response = await client.get(
        "/api/subway/station/K001/timetable/up/weekdays/00:01:00",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 200
    assert response.json().get("stationID") is not None
    assert response.json().get("startStationID") is not None
    assert response.json().get("terminalStationID") is not None
    assert response.json().get("departureTime") is not None
    assert response.json().get("weekday") is not None
    assert response.json().get("heading") is not None


@pytest.mark.asyncio
async def test_get_subway_timetable_not_exist(
    client: TestClient,
    clean_db,
    create_test_user,
) -> None:
    access_token = await get_access_token(client)

    response = await client.get(
        "/api/subway/station/K001/timetable/up/weekdays/00:01:00",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "TIMETABLE_NOT_FOUND",
    }


@pytest.mark.asyncio
async def test_delete_subway_timetable(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_subway_timetable,
) -> None:
    access_token = await get_access_token(client)

    response = await client.delete(
        "/api/subway/station/K001/timetable/up/weekdays/00:01:00",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_subway_timetable_not_exist(
    client: TestClient,
    clean_db,
    create_test_user,
) -> None:
    access_token = await get_access_token(client)

    response = await client.delete(
        "/api/subway/station/K001/timetable/up/weekdays/00:01:00",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_get_subway_realtime(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_subway_realtime,
) -> None:
    access_token = await get_access_token(client)

    response = await client.get(
        "/api/subway/station/K001/realtime",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("data") is not None
    for item in response_json.get("data"):
        assert item.get("stationID") is not None
        assert item.get("sequence") is not None
        assert item.get("current") is not None
        assert item.get("heading") is not None
        assert item.get("station") is not None
        assert item.get("time") is not None
        assert item.get("trainNumber") is not None
        assert item.get("express") is not None
        assert item.get("terminalStationID") is not None
        assert item.get("last") is not None
        assert item.get("status") is not None
