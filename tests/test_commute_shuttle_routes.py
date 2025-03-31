import pytest
from async_asgi_testclient import TestClient
from sqlalchemy import select

from database import fetch_one
from model.commute_shuttle import CommuteShuttleRoute, CommuteShuttleStop, CommuteShuttleTimetable
from tests.utils import get_access_token


@pytest.mark.asyncio
async def test_get_commute_shuttle_route_list(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_commute_shuttle_route,
) -> None:
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/commute/route",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("data") is not None
    assert len(response_json["data"]) > 0
    for route in response_json["data"]:
        assert route.get("name") is not None
        assert route.get("korean") is not None
        assert route.get("english") is not None


@pytest.mark.asyncio
async def test_create_commute_shuttle_route(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_commute_shuttle_route,
) -> None:
    access_token = await get_access_token(client)
    route_name = "test_route"
    route_description_korean = "테스트 노선"
    route_description_english = "Test Route"
    response = await client.post(
        "/api/commute/route",
        json={
            "name": route_name,
            "korean": route_description_korean,
            "english": route_description_english,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 201
    response_json = response.json()
    assert response_json.get("name") == route_name
    assert response_json.get("korean") == route_description_korean
    assert response_json.get("english") == route_description_english
    check_statement = select(CommuteShuttleRoute).where(
        CommuteShuttleRoute.name == route_name
    )
    query_result = await fetch_one(check_statement)
    assert query_result is not None
    assert query_result.name == route_name


@pytest.mark.asyncio
async def test_create_commute_shuttle_route_duplicate_name(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_commute_shuttle_route,
) -> None:
    access_token = await get_access_token(client)
    route_name = "test_route1"
    route_description_korean = "테스트 노선"
    route_description_english = "Test Route"
    response = await client.post(
        "/api/commute/route",
        json={
            "name": route_name,
            "korean": route_description_korean,
            "english": route_description_english,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 409
    assert response.json().get("detail") == "DUPLICATE_ROUTE_NAME"


@pytest.mark.asyncio
async def test_create_commute_shuttle_route_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from commute_shuttle import service

    async def mock_create_route(*args, **kwargs) -> None:
        return None

    monkeypatch.setattr(service, "create_route", mock_create_route)

    access_token = await get_access_token(client)
    route_name = "test_route"
    route_description_korean = "테스트 노선"
    route_description_english = "Test Route"
    response = await client.post(
        "/api/commute/route",
        json={
            "name": route_name,
            "korean": route_description_korean,
            "english": route_description_english,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 500
    assert response.json().get("detail") == "INTERNAL_SERVER_ERROR"


@pytest.mark.asyncio
async def test_get_commute_shuttle_route_detail(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_commute_shuttle_route,
) -> None:
    access_token = await get_access_token(client)
    route_name = "test_route1"
    response = await client.get(
        f"/api/commute/route/{route_name}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("name") == route_name
    assert response_json.get("korean") is not None
    assert response_json.get("english") is not None


@pytest.mark.asyncio
async def test_get_commute_shuttle_route_detail_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_commute_shuttle_route,
) -> None:
    access_token = await get_access_token(client)
    route_name = "test_route"
    response = await client.get(
        f"/api/commute/route/{route_name}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json().get("detail") == "ROUTE_NOT_FOUND"


@pytest.mark.asyncio
async def test_update_commute_shuttle_route(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_commute_shuttle_route,
) -> None:
    access_token = await get_access_token(client)
    route_name = "test_route1"
    route_description_korean = "테스트 노선"
    route_description_english = "Test Route"
    response = await client.put(
        f"/api/commute/route/{route_name}",
        json={
            "korean": route_description_korean,
            "english": route_description_english,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("name") == route_name
    assert response_json.get("korean") == route_description_korean
    assert response_json.get("english") == route_description_english


@pytest.mark.asyncio
async def test_update_commute_shuttle_route_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_commute_shuttle_route,
) -> None:
    access_token = await get_access_token(client)
    route_name = "test_route"
    route_description_korean = "테스트 노선"
    route_description_english = "Test Route"
    response = await client.put(
        f"/api/commute/route/{route_name}",
        json={
            "korean": route_description_korean,
            "english": route_description_english,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json().get("detail") == "ROUTE_NOT_FOUND"


@pytest.mark.asyncio
async def test_update_commute_shuttle_route_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_commute_shuttle_route,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from commute_shuttle import service

    async def mock_update_route(*args, **kwargs) -> None:
        return None

    monkeypatch.setattr(service, "update_route", mock_update_route)

    access_token = await get_access_token(client)
    route_name = "test_route1"
    route_description_korean = "테스트 노선"
    route_description_english = "Test Route"
    response = await client.put(
        f"/api/commute/route/{route_name}",
        json={
            "korean": route_description_korean,
            "english": route_description_english,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 500
    assert response.json().get("detail") == "INTERNAL_SERVER_ERROR"


@pytest.mark.asyncio
async def test_delete_commute_shuttle_route(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_commute_shuttle_route,
) -> None:
    access_token = await get_access_token(client)
    route_name = "test_route1"
    response = await client.delete(
        f"/api/commute/route/{route_name}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_commute_shuttle_route_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_commute_shuttle_route,
) -> None:
    access_token = await get_access_token(client)
    route_name = "test_route"
    response = await client.delete(
        f"/api/commute/route/{route_name}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json().get("detail") == "ROUTE_NOT_FOUND"


@pytest.mark.asyncio
async def test_get_commute_shuttle_stop_list(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_commute_shuttle_stop,
) -> None:
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/commute/stop",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("data") is not None
    assert len(response_json["data"]) > 0
    for stop in response_json["data"]:
        assert stop.get("name") is not None
        assert stop.get("description") is not None
        assert stop.get("latitude") is not None
        assert stop.get("longitude") is not None


@pytest.mark.asyncio
async def test_create_commute_shuttle_stop(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_commute_shuttle_stop,
) -> None:
    access_token = await get_access_token(client)
    stop_name = "test_stop"
    stop_description = "테스트 정류장"
    stop_latitude = 89.0
    stop_longitude = 89.0
    response = await client.post(
        "/api/commute/stop",
        json={
            "name": stop_name,
            "description": stop_description,
            "latitude": stop_latitude,
            "longitude": stop_longitude,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 201
    response_json = response.json()
    assert response_json.get("name") == stop_name
    assert response_json.get("description") == stop_description
    assert response_json.get("latitude") == stop_latitude
    assert response_json.get("longitude") == stop_longitude
    check_statement = select(CommuteShuttleStop).where(
        CommuteShuttleStop.name == stop_name
    )
    query_result = await fetch_one(check_statement)
    assert query_result is not None
    assert query_result.name == stop_name


@pytest.mark.asyncio
async def test_create_commute_shuttle_stop_duplicate_name(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_commute_shuttle_stop,
) -> None:
    access_token = await get_access_token(client)
    stop_name = "test_stop1"
    stop_description = "테스트 정류장"
    stop_latitude = 89.0
    stop_longitude = 89.0
    response = await client.post(
        "/api/commute/stop",
        json={
            "name": stop_name,
            "description": stop_description,
            "latitude": stop_latitude,
            "longitude": stop_longitude,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 409
    assert response.json().get("detail") == "DUPLICATE_STOP_NAME"


@pytest.mark.asyncio
async def test_create_commute_shuttle_stop_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from commute_shuttle import service

    async def mock_create_stop(*args, **kwargs) -> None:
        return None

    monkeypatch.setattr(service, "create_stop", mock_create_stop)

    access_token = await get_access_token(client)
    stop_name = "test_stop"
    stop_description = "테스트 정류장"
    stop_latitude = 89.0
    stop_longitude = 89.0
    response = await client.post(
        "/api/commute/stop",
        json={
            "name": stop_name,
            "description": stop_description,
            "latitude": stop_latitude,
            "longitude": stop_longitude,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 500
    assert response.json().get("detail") == "INTERNAL_SERVER_ERROR"


@pytest.mark.asyncio
async def test_get_commute_shuttle_stop_detail(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_commute_shuttle_stop,
) -> None:
    access_token = await get_access_token(client)
    stop_name = "test_stop1"
    response = await client.get(
        f"/api/commute/stop/{stop_name}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("name") == stop_name
    assert response_json.get("description") is not None
    assert response_json.get("latitude") is not None
    assert response_json.get("longitude") is not None


@pytest.mark.asyncio
async def test_get_commute_shuttle_stop_detail_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_commute_shuttle_stop,
) -> None:
    access_token = await get_access_token(client)
    stop_name = "test_stop"
    response = await client.get(
        f"/api/commute/stop/{stop_name}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json().get("detail") == "STOP_NOT_FOUND"


@pytest.mark.asyncio
async def test_update_commute_shuttle_stop(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_commute_shuttle_stop,
) -> None:
    access_token = await get_access_token(client)
    stop_name = "test_stop1"
    stop_description = "테스트 정류장"
    stop_latitude = 89.0
    stop_longitude = 89.0
    response = await client.put(
        f"/api/commute/stop/{stop_name}",
        json={
            "description": stop_description,
            "latitude": stop_latitude,
            "longitude": stop_longitude,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("name") == stop_name
    assert response_json.get("description") == stop_description
    assert response_json.get("latitude") == stop_latitude
    assert response_json.get("longitude") == stop_longitude


@pytest.mark.asyncio
async def test_update_commute_shuttle_stop_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_commute_shuttle_stop,
) -> None:
    access_token = await get_access_token(client)
    stop_name = "test_stop"
    stop_description = "테스트 정류장"
    stop_latitude = 89.0
    stop_longitude = 89.0
    response = await client.put(
        f"/api/commute/stop/{stop_name}",
        json={
            "description": stop_description,
            "latitude": stop_latitude,
            "longitude": stop_longitude,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json().get("detail") == "STOP_NOT_FOUND"


@pytest.mark.asyncio
async def test_update_commute_shuttle_stop_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_commute_shuttle_stop,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from commute_shuttle import service

    async def mock_update_stop(*args, **kwargs) -> None:
        return None

    monkeypatch.setattr(service, "update_stop", mock_update_stop)

    access_token = await get_access_token(client)
    stop_name = "test_stop1"
    stop_description = "테스트 정류장"
    stop_latitude = 89.0
    stop_longitude = 89.0
    response = await client.put(
        f"/api/commute/stop/{stop_name}",
        json={
            "description": stop_description,
            "latitude": stop_latitude,
            "longitude": stop_longitude,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 500
    assert response.json().get("detail") == "INTERNAL_SERVER_ERROR"


@pytest.mark.asyncio
async def test_delete_commute_shuttle_stop(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_commute_shuttle_stop,
) -> None:
    access_token = await get_access_token(client)
    stop_name = "test_stop1"
    response = await client.delete(
        f"/api/commute/stop/{stop_name}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_commute_shuttle_stop_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_commute_shuttle_stop,
) -> None:
    access_token = await get_access_token(client)
    stop_name = "test_stop"
    response = await client.delete(
        f"/api/commute/stop/{stop_name}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json().get("detail") == "STOP_NOT_FOUND"


@pytest.mark.asyncio
async def test_get_commute_shuttle_timetable_list(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_commute_shuttle_timetable,
) -> None:
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/commute/timetable",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("data") is not None
    assert len(response_json["data"]) > 0
    for timetable in response_json["data"]:
        assert timetable.get("stop") is not None
        assert timetable.get("name") is not None
        assert timetable.get("sequence") is not None
        assert timetable.get("time") is not None


@pytest.mark.asyncio
async def test_get_commute_shuttle_timetable_list_filter(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_commute_shuttle_timetable,
) -> None:
    access_token = await get_access_token(client)
    route_name = "test_route1"
    response = await client.get(
        f"/api/commute/timetable?route={route_name}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("data") is not None
    assert len(response_json["data"]) > 0
    for timetable in response_json["data"]:
        assert timetable.get("stop") is not None
        assert timetable.get("name") == route_name
        assert timetable.get("sequence") is not None
        assert timetable.get("time") is not None


@pytest.mark.asyncio
async def test_create_commute_shuttle_timetable(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_commute_shuttle_route,
    create_test_commute_shuttle_stop,
) -> None:
    access_token = await get_access_token(client)
    route_name = "test_route1"
    stop_name = "test_stop1"
    sequence = 1
    departure_time = "09:00"
    response = await client.post(
        "/api/commute/timetable",
        json={
            "route": route_name,
            "stop": stop_name,
            "sequence": sequence,
            "time": departure_time,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 201
    response_json = response.json()
    assert response_json.get("name") == route_name
    assert response_json.get("stop") == stop_name
    assert response_json.get("sequence") == sequence
    assert response_json.get("time") is not None
    check_statement = select(CommuteShuttleTimetable).where(
        CommuteShuttleTimetable.route_name == route_name
    )
    query_result = await fetch_one(check_statement)
    assert query_result is not None
    assert query_result.route_name == route_name


@pytest.mark.asyncio
async def test_create_commute_shuttle_timetable_duplicate_sequence(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_commute_shuttle_timetable,
) -> None:
    access_token = await get_access_token(client)
    route_name = "test_route1"
    stop_name = "test_stop1"
    sequence = 1
    departure_time = "09:00"
    response = await client.post(
        "/api/commute/timetable",
        json={
            "route": route_name,
            "stop": stop_name,
            "sequence": sequence,
            "time": departure_time,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 409
    assert response.json().get("detail") == "DUPLICATE_TIMETABLE_SEQUENCE"


@pytest.mark.asyncio
async def test_create_commute_shuttle_timetable_route_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_commute_shuttle_stop,
) -> None:
    access_token = await get_access_token(client)
    route_name = "test_route"
    stop_name = "test_stop1"
    sequence = 1
    departure_time = "09:00"
    response = await client.post(
        "/api/commute/timetable",
        json={
            "route": route_name,
            "stop": stop_name,
            "sequence": sequence,
            "time": departure_time,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json().get("detail") == "ROUTE_NOT_FOUND"


@pytest.mark.asyncio
async def test_create_commute_shuttle_timetable_stop_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_commute_shuttle_route,
) -> None:
    access_token = await get_access_token(client)
    route_name = "test_route1"
    stop_name = "test_stop"
    sequence = 1
    departure_time = "09:00"
    response = await client.post(
        "/api/commute/timetable",
        json={
            "route": route_name,
            "stop": stop_name,
            "sequence": sequence,
            "time": departure_time,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json().get("detail") == "STOP_NOT_FOUND"


@pytest.mark.asyncio
async def test_create_commute_shuttle_timetable_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_commute_shuttle_route,
    create_test_commute_shuttle_stop,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from commute_shuttle import service

    async def mock_create_timetable(*args, **kwargs) -> None:
        return None

    monkeypatch.setattr(service, "create_timetable", mock_create_timetable)

    access_token = await get_access_token(client)
    route_name = "test_route1"
    stop_name = "test_stop1"
    sequence = 1
    departure_time = "09:00"
    response = await client.post(
        "/api/commute/timetable",
        json={
            "route": route_name,
            "stop": stop_name,
            "sequence": sequence,
            "time": departure_time,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 500
    assert response.json().get("detail") == "INTERNAL_SERVER_ERROR"


@pytest.mark.asyncio
async def test_get_commute_shuttle_timetable_detail(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_commute_shuttle_timetable,
) -> None:
    access_token = await get_access_token(client)
    route_name = "test_route1"
    stop_name = "test_stop1"
    response = await client.get(
        f"/api/commute/timetable/{route_name}/{stop_name}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("name") == route_name
    assert response_json.get("stop") == stop_name
    assert response_json.get("sequence") is not None
    assert response_json.get("time") is not None


@pytest.mark.asyncio
async def test_get_commute_shuttle_timetable_detail_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_commute_shuttle_timetable,
) -> None:
    access_token = await get_access_token(client)
    route_name = "test_route1"
    stop_name = "test_stop10"
    response = await client.get(
        f"/api/commute/timetable/{route_name}/{stop_name}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json().get("detail") == "TIMETABLE_NOT_FOUND"


@pytest.mark.asyncio
async def test_update_commute_shuttle_timetable(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_commute_shuttle_timetable,
) -> None:
    access_token = await get_access_token(client)
    route_name = "test_route1"
    stop_name = "test_stop1"
    sequence = 1
    departure_time = "09:00"
    response = await client.put(
        f"/api/commute/timetable/{route_name}/{stop_name}",
        json={
            "sequence": sequence,
            "time": departure_time,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("name") == route_name
    assert response_json.get("stop") == stop_name
    assert response_json.get("sequence") == sequence
    assert response_json.get("time") is not None


@pytest.mark.asyncio
async def test_update_commute_shuttle_timetable_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_commute_shuttle_timetable,
) -> None:
    access_token = await get_access_token(client)
    route_name = "test_route1"
    stop_name = "test_stop10"
    sequence = 1
    departure_time = "09:00"
    response = await client.put(
        f"/api/commute/timetable/{route_name}/{stop_name}",
        json={
            "sequence": sequence,
            "time": departure_time,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json().get("detail") == "TIMETABLE_NOT_FOUND"


@pytest.mark.asyncio
async def test_update_commute_shuttle_timetable_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_commute_shuttle_timetable,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from commute_shuttle import service

    async def mock_update_timetable(*args, **kwargs) -> None:
        return None

    monkeypatch.setattr(service, "update_timetable", mock_update_timetable)

    access_token = await get_access_token(client)
    route_name = "test_route1"
    stop_name = "test_stop1"
    sequence = 1
    departure_time = "09:00"
    response = await client.put(
        f"/api/commute/timetable/{route_name}/{stop_name}",
        json={
            "sequence": sequence,
            "time": departure_time,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 500
    assert response.json().get("detail") == "INTERNAL_SERVER_ERROR"


@pytest.mark.asyncio
async def test_delete_commute_shuttle_timetable(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_commute_shuttle_timetable,
) -> None:
    access_token = await get_access_token(client)
    route_name = "test_route1"
    stop_name = "test_stop1"
    response = await client.delete(
        f"/api/commute/timetable/{route_name}/{stop_name}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 204
