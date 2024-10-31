import datetime

import pytest
from async_asgi_testclient import TestClient
from sqlalchemy import select

from database import fetch_one
from model.shuttle import ShuttleHoliday, ShuttlePeriod, ShuttleRoute, ShuttleStop, ShuttleRouteStop, ShuttleTimetable
from tests.utils import get_access_token


@pytest.mark.asyncio
async def test_get_shuttle_holiday(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_holiday,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/shuttle/holiday",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json.get("data")) > 0
    for holiday in response_json.get("data"):
        assert holiday.get("calendar") is not None
        assert holiday.get("date") is not None
        assert holiday.get("type") is not None


@pytest.mark.asyncio
async def test_get_shuttle_holiday_filter_calendar(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_holiday,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/shuttle/holiday?calendar=solar",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json.get("data")) > 0
    for holiday in response_json.get("data"):
        assert holiday.get("calendar") == "solar"
        assert holiday.get("date") is not None
        assert holiday.get("type") is not None


@pytest.mark.asyncio
async def test_get_shuttle_holiday_filter_date(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_holiday,
):
    access_token = await get_access_token(client)
    response = await client.get(
        f"/api/shuttle/holiday?date={datetime.datetime.now().date().strftime('%Y-%m-%d')}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json.get("data")) > 0
    for holiday in response_json.get("data"):
        assert holiday.get("calendar") is not None
        assert holiday.get("date") == datetime.datetime.now().date().strftime(
            "%Y-%m-%d",
        )


@pytest.mark.asyncio
async def test_get_shuttle_holiday_filter_start_date(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_holiday,
):
    access_token = await get_access_token(client)
    response = await client.get(
        f"/api/shuttle/holiday?start={datetime.datetime.now().date().strftime('%Y-%m-%d')}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json.get("data")) > 0
    for holiday in response_json.get("data"):
        assert holiday.get("calendar") is not None
        assert holiday.get("date") >= datetime.datetime.now().date().strftime(
            "%Y-%m-%d",
        )


@pytest.mark.asyncio
async def test_get_shuttle_holiday_filter_end_date(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_holiday,
):
    access_token = await get_access_token(client)
    response = await client.get(
        f"/api/shuttle/holiday?end={datetime.datetime.now().date().strftime('%Y-%m-%d')}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json.get("data")) > 0
    for holiday in response_json.get("data"):
        assert holiday.get("calendar") is not None
        assert holiday.get("date") <= datetime.datetime.now().date().strftime(
            "%Y-%m-%d",
        )


@pytest.mark.asyncio
async def test_create_shuttle_holiday(
    client: TestClient,
    clean_db,
    create_test_user,
):
    access_token = await get_access_token(client)
    response = await client.post(
        "/api/shuttle/holiday",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "calendar": "lunar",
            "date": "2021-01-01",
            "type": "weekends",
        },
    )
    assert response.status_code == 201
    response_json = response.json()
    assert response_json.get("calendar") == "lunar"
    assert response_json.get("date") == "2021-01-01"
    assert response_json.get("type") == "weekends"
    check_statement = select(ShuttleHoliday).where(
        ShuttleHoliday.calendar == "lunar",
        ShuttleHoliday.type_ == "weekends",
    )
    query_result = await fetch_one(check_statement)
    assert query_result is not None


@pytest.mark.asyncio
async def test_create_shuttle_holiday_duplicate(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_holiday,
):
    access_token = await get_access_token(client)
    response = await client.post(
        "/api/shuttle/holiday",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "calendar": "solar",
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "type": "weekends",
        },
    )
    assert response.status_code == 409
    response_json = response.json()
    assert response_json.get("detail") == "DUPLICATE_HOLIDAY_DATE"


@pytest.mark.asyncio
async def test_create_shuttle_holiday_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    monkeypatch: pytest.MonkeyPatch,
):
    from shuttle import service

    async def mock_create_holiday(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "create_holiday", mock_create_holiday)

    access_token = await get_access_token(client)
    response = await client.post(
        "/api/shuttle/holiday",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "calendar": "lunar",
            "date": "2021-01-01",
            "type": "weekends",
        },
    )
    assert response.status_code == 500
    response_json = response.json()
    assert response_json.get("detail") == "INTERNAL_SERVER_ERROR"


@pytest.mark.asyncio
async def test_get_shuttle_holiday_item(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_holiday,
):
    access_token = await get_access_token(client)
    response = await client.get(
        f"/api/shuttle/holiday/solar/{datetime.datetime.now().date()}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("calendar") is not None
    assert response_json.get("date") is not None
    assert response_json.get("type") is not None


@pytest.mark.asyncio
async def test_get_shuttle_holiday_item_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_holiday,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/shuttle/holiday/solar/2099-01-01",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    response_json = response.json()
    assert response_json.get("detail") == "HOLIDAY_NOT_FOUND"


@pytest.mark.asyncio
async def test_delete_shuttle_holiday_item(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_holiday,
):
    access_token = await get_access_token(client)
    response = await client.delete(
        f"/api/shuttle/holiday/solar/{datetime.datetime.now().date()}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_shuttle_holiday_item_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_holiday,
):
    access_token = await get_access_token(client)
    response = await client.delete(
        "/api/shuttle/holiday/solar/2099-01-01",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    response_json = response.json()
    assert response_json.get("detail") == "HOLIDAY_NOT_FOUND"


@pytest.mark.asyncio
async def test_get_shuttle_period(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_period,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/shuttle/period",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json.get("data")) > 0
    for period in response_json.get("data"):
        assert period.get("type") is not None
        assert period.get("start") is not None
        assert period.get("end") is not None


@pytest.mark.asyncio
async def test_get_shuttle_period_filter_type(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_period,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/shuttle/period?period=semester",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json.get("data")) > 0
    for period in response_json.get("data"):
        assert period.get("type") == "semester"
        assert period.get("start") is not None
        assert period.get("end") is not None


@pytest.mark.asyncio
async def test_get_shuttle_period_filter_date(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_period,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/shuttle/period?date=2024-01-15",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json.get("data")) > 0
    for period in response_json.get("data"):
        assert period.get("type") == "semester"
        assert period.get("start") <= "2024-01-15"
        assert period.get("end") >= "2024-01-15"


@pytest.mark.asyncio
async def test_create_shuttle_period(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_period_type,
):
    access_token = await get_access_token(client)
    response = await client.post(
        "/api/shuttle/period",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "type": "semester",
            "start": "2021-01-01",
            "end": "2021-01-31",
        },
    )
    assert response.status_code == 201
    response_json = response.json()
    assert response_json.get("type") == "semester"
    assert response_json.get("start") is not None
    assert response_json.get("end") is not None
    check_statement = select(ShuttlePeriod).where(
        ShuttlePeriod.type_id == "semester",
        ShuttlePeriod.start == "2021-01-01",
        ShuttlePeriod.end == "2021-01-31",
    )
    query_result = await fetch_one(check_statement)
    assert query_result is not None


@pytest.mark.asyncio
async def test_create_shuttle_period_duplicate(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_period,
):
    access_token = await get_access_token(client)
    response = await client.post(
        "/api/shuttle/period",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "type": "semester",
            "start": "2024-01-01",
            "end": "2024-02-01",
        },
    )
    assert response.status_code == 409
    response_json = response.json()
    assert response_json.get("detail") == "DUPLICATE_PERIOD"


@pytest.mark.asyncio
async def test_create_shuttle_period_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    monkeypatch: pytest.MonkeyPatch,
):
    from shuttle import service

    async def mock_create_period(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "create_period", mock_create_period)

    access_token = await get_access_token(client)
    response = await client.post(
        "/api/shuttle/period",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "type": "weekdays",
            "start": "2021-01-01",
            "end": "2021-01-31",
        },
    )
    assert response.status_code == 500
    response_json = response.json()
    assert response_json.get("detail") == "INTERNAL_SERVER_ERROR"


@pytest.mark.asyncio
async def test_get_shuttle_period_item(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_period,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/shuttle/period/semester/2024-01-01/2024-02-01",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("type") is not None
    assert response_json.get("start") is not None
    assert response_json.get("end") is not None


@pytest.mark.asyncio
async def test_get_shuttle_period_item_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_period,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/shuttle/period/semester/2099-01-01/2099-01-31",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    response_json = response.json()
    assert response_json.get("detail") == "PERIOD_NOT_FOUND"


@pytest.mark.asyncio
async def test_delete_shuttle_period_item(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_period,
):
    access_token = await get_access_token(client)
    response = await client.delete(
        "/api/shuttle/period/semester/2024-01-01/2024-02-01",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_shuttle_period_item_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_period,
):
    access_token = await get_access_token(client)
    response = await client.delete(
        "/api/shuttle/period/semester/2099-01-01/2099-01-31",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    response_json = response.json()
    assert response_json.get("detail") == "PERIOD_NOT_FOUND"


@pytest.mark.asyncio
async def test_get_shuttle_route(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_route,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/shuttle/route",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json.get("data")) > 0
    for route in response_json.get("data"):
        assert route.get("name") is not None
        assert route.get("tag") is not None


@pytest.mark.asyncio
async def test_get_shuttle_route_filter_name(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_route,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/shuttle/route?name=test_route1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json.get("data")) > 0
    for route in response_json.get("data"):
        assert route.get("name") == "test_route1"
        assert route.get("tag") is not None


@pytest.mark.asyncio
async def test_get_shuttle_route_filter_tag(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_route,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/shuttle/route?tag=test_tag",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json.get("data")) > 0
    for route in response_json.get("data"):
        assert route.get("name") is not None
        assert route.get("tag") == "test_tag"


@pytest.mark.asyncio
async def test_create_shuttle_route(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_stop,
):
    access_token = await get_access_token(client)
    response = await client.post(
        "/api/shuttle/route",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "name": "test",
            "tag": "test",
            "korean": "테스트",
            "english": "test",
            "start": "test_stop1",
            "end": "test_stop2",
        },
    )
    assert response.status_code == 201
    response_json = response.json()
    assert response_json.get("name") == "test"
    assert response_json.get("tag") == "test"
    assert response_json.get("korean") == "테스트"
    assert response_json.get("english") == "test"
    assert response_json.get("start") == "test_stop1"
    assert response_json.get("end") == "test_stop2"
    check_statement = select(ShuttleRoute).where(
        ShuttleRoute.name == "test",
        ShuttleRoute.tag == "test",
        ShuttleRoute.korean == "테스트",
        ShuttleRoute.english == "test"
    )
    query_result = await fetch_one(check_statement)
    assert query_result is not None


@pytest.mark.asyncio
async def test_create_shuttle_route_duplicate(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_route,
):
    access_token = await get_access_token(client)
    response = await client.post(
        "/api/shuttle/route",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "name": "test_route1",
            "tag": "test",
            "korean": "테스트",
            "english": "test",
            "start": "test_stop1",
            "end": "test_stop2",
        },
    )
    assert response.status_code == 409
    response_json = response.json()
    assert response_json.get("detail") == "DUPLICATE_ROUTE_NAME"


@pytest.mark.asyncio
async def test_create_shuttle_route_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_stop,
    monkeypatch: pytest.MonkeyPatch,
):
    from shuttle import service

    async def mock_create_route(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "create_route", mock_create_route)

    access_token = await get_access_token(client)
    response = await client.post(
        "/api/shuttle/route",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "name": "test",
            "tag": "test",
            "korean": "테스트",
            "english": "test",
            "start": "test_stop1",
            "end": "test_stop2",
        },
    )
    assert response.status_code == 500
    response_json = response.json()
    assert response_json.get("detail") == "INTERNAL_SERVER_ERROR"


@pytest.mark.asyncio
async def test_get_shuttle_route_item(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_route,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/shuttle/route/test_route1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("name") is not None
    assert response_json.get("tag") is not None
    assert response_json.get("korean") is not None
    assert response_json.get("english") is not None
    assert response_json.get("start") is not None
    assert response_json.get("end") is not None


@pytest.mark.asyncio
async def test_get_shuttle_route_item_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_route,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/shuttle/route/test_route10",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    response_json = response.json()
    assert response_json.get("detail") == "ROUTE_NOT_FOUND"


@pytest.mark.asyncio
async def test_update_shuttle_route_item(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_route,
):
    access_token = await get_access_token(client)
    response = await client.patch(
        "/api/shuttle/route/test_route1",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "tag": "test",
            "korean": "테스트",
            "english": "test",
            "start": "test_stop1",
            "end": "test_stop2",
        },
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("name") is not None
    assert response_json.get("tag") is not None
    assert response_json.get("korean") is not None
    assert response_json.get("english") is not None
    assert response_json.get("start") is not None
    assert response_json.get("end") is not None


@pytest.mark.asyncio
async def test_update_shuttle_route_item_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_route,
):
    access_token = await get_access_token(client)
    response = await client.patch(
        "/api/shuttle/route/test_route10",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "tag": "test",
            "korean": "테스트",
            "english": "test",
            "start": "test_stop1",
            "end": "test_stop2",
        },
    )
    assert response.status_code == 404
    response_json = response.json()
    assert response_json.get("detail") == "ROUTE_NOT_FOUND"


@pytest.mark.asyncio
async def test_update_shuttle_route_item_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_route,
    monkeypatch: pytest.MonkeyPatch,
):
    from shuttle import service

    async def mock_update_route(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "update_route", mock_update_route)

    access_token = await get_access_token(client)
    response = await client.patch(
        "/api/shuttle/route/test_route1",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "tag": "test",
            "korean": "테스트",
            "english": "test",
            "start": "test_stop1",
            "end": "test_stop2",
        },
    )
    assert response.status_code == 500
    response_json = response.json()
    assert response_json.get("detail") == "INTERNAL_SERVER_ERROR"


@pytest.mark.asyncio
async def test_delete_shuttle_route_item(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_route,
):
    access_token = await get_access_token(client)
    response = await client.delete(
        "/api/shuttle/route/test_route1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_shuttle_route_item_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_route,
):
    access_token = await get_access_token(client)
    response = await client.delete(
        "/api/shuttle/route/test_route10",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    response_json = response.json()
    assert response_json.get("detail") == "ROUTE_NOT_FOUND"


@pytest.mark.asyncio
async def test_get_shuttle_stop(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_stop,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/shuttle/stop",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json.get("data")) > 0
    for stop in response_json.get("data"):
        assert stop.get("name") is not None
        assert stop.get("latitude") is not None
        assert stop.get("longitude") is not None


@pytest.mark.asyncio
async def test_get_shuttle_stop_filter_name(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_stop,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/shuttle/stop?name=test_stop1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json.get("data")) > 0
    for stop in response_json.get("data"):
        assert "test_stop1" in stop.get("name")
        assert stop.get("latitude") is not None
        assert stop.get("longitude") is not None


@pytest.mark.asyncio
async def test_create_shuttle_stop(
    client: TestClient,
    clean_db,
    create_test_user,
):
    access_token = await get_access_token(client)
    response = await client.post(
        "/api/shuttle/stop",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "name": "test_stop3",
            "latitude": 37.000000,
            "longitude": 127.000000,
        },
    )
    assert response.status_code == 201
    response_json = response.json()
    assert response_json.get("name") == "test_stop3"
    assert response_json.get("latitude") == 37.000000
    assert response_json.get("longitude") == 127.000000
    check_statement = select(ShuttleStop).where(
        ShuttleStop.name == "test_stop3"
    )
    query_result = await fetch_one(check_statement)
    assert query_result is not None


@pytest.mark.asyncio
async def test_create_shuttle_stop_duplicate(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_stop,
):
    access_token = await get_access_token(client)
    response = await client.post(
        "/api/shuttle/stop",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "name": "test_stop1",
            "latitude": 37.000000,
            "longitude": 127.000000,
        },
    )
    assert response.status_code == 409
    response_json = response.json()
    assert response_json.get("detail") == "DUPLICATE_STOP_NAME"


@pytest.mark.asyncio
async def test_create_shuttle_stop_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    monkeypatch: pytest.MonkeyPatch,
):
    from shuttle import service

    async def mock_create_stop(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "create_stop", mock_create_stop)

    access_token = await get_access_token(client)
    response = await client.post(
        "/api/shuttle/stop",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "name": "test_stop3",
            "latitude": 37.000000,
            "longitude": 127.000000,
        },
    )
    assert response.status_code == 500
    response_json = response.json()
    assert response_json.get("detail") == "INTERNAL_SERVER_ERROR"


@pytest.mark.asyncio
async def test_get_shuttle_stop_item(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_stop,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/shuttle/stop/test_stop1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("name") is not None
    assert response_json.get("latitude") is not None
    assert response_json.get("longitude") is not None


@pytest.mark.asyncio
async def test_get_shuttle_stop_item_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_stop,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/shuttle/stop/test_stop10",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    response_json = response.json()
    assert response_json.get("detail") == "STOP_NOT_FOUND"


@pytest.mark.asyncio
async def test_update_shuttle_stop_item(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_stop,
):
    access_token = await get_access_token(client)
    response = await client.patch(
        "/api/shuttle/stop/test_stop1",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "latitude": 37.000000,
            "longitude": 127.000000,
        },
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("name") is not None
    assert response_json.get("latitude") is not None
    assert response_json.get("longitude") is not None


@pytest.mark.asyncio
async def test_update_shuttle_stop_item_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_stop,
):
    access_token = await get_access_token(client)
    response = await client.patch(
        "/api/shuttle/stop/test_stop10",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "latitude": 37.000000,
            "longitude": 127.000000,
        },
    )
    assert response.status_code == 404
    response_json = response.json()
    assert response_json.get("detail") == "STOP_NOT_FOUND"


@pytest.mark.asyncio
async def test_update_shuttle_stop_item_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_stop,
    monkeypatch: pytest.MonkeyPatch,
):
    from shuttle import service

    async def mock_update_stop(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "update_stop", mock_update_stop)

    access_token = await get_access_token(client)
    response = await client.patch(
        "/api/shuttle/stop/test_stop1",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "latitude": 37.000000,
            "longitude": 127.000000,
        },
    )
    assert response.status_code == 500
    response_json = response.json()
    assert response_json.get("detail") == "INTERNAL_SERVER_ERROR"


@pytest.mark.asyncio
async def test_delete_shuttle_stop_item(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_stop,
):
    access_token = await get_access_token(client)
    response = await client.delete(
        "/api/shuttle/stop/test_stop1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_shuttle_stop_item_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_stop,
):
    access_token = await get_access_token(client)
    response = await client.delete(
        "/api/shuttle/stop/test_stop10",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    response_json = response.json()
    assert response_json.get("detail") == "STOP_NOT_FOUND"


@pytest.mark.asyncio
async def test_get_shuttle_route_stop(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_route_stop,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/shuttle/route/test_route1/stop",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json.get("data")) > 0
    for route_stop in response_json.get("data"):
        assert route_stop.get("route") is not None
        assert route_stop.get("stop") is not None
        assert route_stop.get("sequence") is not None
        assert route_stop.get("cumulativeTime") is not None


@pytest.mark.asyncio
async def test_create_shuttle_route_stop(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_route,
    create_test_shuttle_stop,
):
    access_token = await get_access_token(client)
    response = await client.post(
        "/api/shuttle/route/test_route1/stop",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "stop": "test_stop3",
            "sequence": 3,
            "cumulativeTime": "00:10:00",
        },
    )
    assert response.status_code == 201
    response_json = response.json()
    assert response_json.get("route") == "test_route1"
    assert response_json.get("stop") == "test_stop3"
    assert response_json.get("sequence") == 3
    assert response_json.get("cumulativeTime") == "00:10:00"
    check_statement = select(ShuttleRouteStop).where(
        ShuttleRouteStop.route_name == "test_route1",
        ShuttleRouteStop.stop_name == "test_stop3",
        ShuttleRouteStop.sequence == 3,
        ShuttleRouteStop.cumulative_time == "00:10:00",
    )
    query_result = await fetch_one(check_statement)
    assert query_result is not None


@pytest.mark.asyncio
async def test_create_shuttle_route_stop_duplicate(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_route_stop,
):
    access_token = await get_access_token(client)
    response = await client.post(
        "/api/shuttle/route/test_route1/stop",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "stop": "test_stop1",
            "sequence": 3,
            "cumulativeTime": "00:10:00",
        },
    )
    assert response.status_code == 409
    response_json = response.json()
    assert response_json.get("detail") == "DUPLICATE_ROUTE_STOP"


@pytest.mark.asyncio
async def test_create_shuttle_route_stop_route_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_route_stop,
):
    access_token = await get_access_token(client)
    response = await client.post(
        "/api/shuttle/route/test_route100/stop",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "stop": "test_stop1",
            "sequence": 3,
            "cumulativeTime": "00:10:00",
        },
    )
    assert response.status_code == 404
    response_json = response.json()
    assert response_json.get("detail") == "ROUTE_NOT_FOUND"


@pytest.mark.asyncio
async def test_create_shuttle_route_stop_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_route,
    create_test_shuttle_stop,
    monkeypatch: pytest.MonkeyPatch,
):
    from shuttle import service

    async def mock_create_route_stop(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "create_route_stop", mock_create_route_stop)

    access_token = await get_access_token(client)
    response = await client.post(
        "/api/shuttle/route/test_route1/stop",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "stop": "test_stop3",
            "sequence": 3,
            "cumulativeTime": "00:10:00",
        },
    )
    assert response.status_code == 500
    response_json = response.json()
    assert response_json.get("detail") == "INTERNAL_SERVER_ERROR"


@pytest.mark.asyncio
async def test_get_shuttle_route_stop_item(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_route_stop,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/shuttle/route/test_route1/stop/test_stop1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("route") is not None
    assert response_json.get("stop") is not None
    assert response_json.get("sequence") is not None
    assert response_json.get("cumulativeTime") is not None


@pytest.mark.asyncio
async def test_get_shuttle_route_stop_item_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_route_stop,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/shuttle/route/test_route1/stop/test_stop9",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    response_json = response.json()
    assert response_json.get("detail") == "ROUTE_STOP_NOT_FOUND"


@pytest.mark.asyncio
async def test_update_shuttle_route_stop_item(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_route_stop,
):
    access_token = await get_access_token(client)
    response = await client.patch(
        "/api/shuttle/route/test_route1/stop/test_stop1",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "sequence": 2,
            "cumulativeTime": "00:10:00",
        },
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("route") is not None
    assert response_json.get("stop") is not None
    assert response_json.get("sequence") is not None
    assert response_json.get("cumulativeTime") is not None


@pytest.mark.asyncio
async def test_update_shuttle_route_stop_item_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_route_stop,
):
    access_token = await get_access_token(client)
    response = await client.patch(
        "/api/shuttle/route/test_route1/stop/test_stop9",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "sequence": 2,
            "cumulativeTime": "00:10:00",
        },
    )
    assert response.status_code == 404
    response_json = response.json()
    assert response_json.get("detail") == "ROUTE_STOP_NOT_FOUND"


@pytest.mark.asyncio
async def test_update_shuttle_route_stop_item_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_route_stop,
    monkeypatch: pytest.MonkeyPatch,
):
    from shuttle import service

    async def mock_update_route_stop(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "update_route_stop", mock_update_route_stop)

    access_token = await get_access_token(client)
    response = await client.patch(
        "/api/shuttle/route/test_route1/stop/test_stop1",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "sequence": 2,
            "cumulativeTime": "00:10:00",
        },
    )
    assert response.status_code == 500
    response_json = response.json()
    assert response_json.get("detail") == "INTERNAL_SERVER_ERROR"


@pytest.mark.asyncio
async def test_delete_shuttle_route_stop_item(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_route_stop,
):
    access_token = await get_access_token(client)
    response = await client.delete(
        "/api/shuttle/route/test_route1/stop/test_stop1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_shuttle_route_stop_item_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_route_stop,
):
    access_token = await get_access_token(client)
    response = await client.delete(
        "/api/shuttle/route/test_route1/stop/test_stop9",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    response_json = response.json()
    assert response_json.get("detail") == "ROUTE_STOP_NOT_FOUND"


@pytest.mark.asyncio
async def test_get_shuttle_timetable(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_timetable,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/shuttle/timetable",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json.get("data")) > 0
    for schedule in response_json.get("data"):
        assert schedule.get("sequence") is not None
        assert schedule.get("period") is not None
        assert schedule.get("weekdays") is not None
        assert schedule.get("route") is not None
        assert schedule.get("time") is not None


@pytest.mark.asyncio
async def test_get_shuttle_timetable_filter_route(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_timetable,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/shuttle/timetable?route=test_route1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json.get("data")) > 0
    for schedule in response_json.get("data"):
        assert schedule.get("sequence") is not None
        assert schedule.get("period") is not None
        assert schedule.get("weekdays") is not None
        assert schedule.get("route") == "test_route1"
        assert schedule.get("time") is not None


@pytest.mark.asyncio
async def test_get_shuttle_timetable_filter_period(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_timetable,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/shuttle/timetable?period=semester",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json.get("data")) > 0
    for schedule in response_json.get("data"):
        assert schedule.get("sequence") is not None
        assert schedule.get("period") == "semester"
        assert schedule.get("weekdays") is not None
        assert schedule.get("route") is not None
        assert schedule.get("time") is not None


@pytest.mark.asyncio
async def test_get_shuttle_timetable_filter_weekdays(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_timetable,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/shuttle/timetable?weekdays=true",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json.get("data")) >= 0
    for schedule in response_json.get("data"):
        assert schedule.get("sequence") is not None
        assert schedule.get("period") is not None
        assert schedule.get("weekdays") is True
        assert schedule.get("route") is not None
        assert schedule.get("time") is not None

    response = await client.get(
        "/api/shuttle/timetable?weekdays=false",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json.get("data")) >= 0
    for schedule in response_json.get("data"):
        assert schedule.get("sequence") is not None
        assert schedule.get("period") is not None
        assert schedule.get("weekdays") is False
        assert schedule.get("route") is not None
        assert schedule.get("time") is not None


@pytest.mark.asyncio
async def test_get_shuttle_timetable_filter_start_time(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_timetable,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/shuttle/timetable?start=00:00",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json.get("data")) > 0
    for schedule in response_json.get("data"):
        assert schedule.get("sequence") is not None
        assert schedule.get("period") is not None
        assert schedule.get("weekdays") is True
        assert schedule.get("route") is not None
        assert schedule.get("time") >= "00:00:00"


@pytest.mark.asyncio
async def test_get_shuttle_timetable_filter_end_time(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_timetable,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/shuttle/timetable?end=05:00",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json.get("data")) > 0
    for schedule in response_json.get("data"):
        assert schedule.get("sequence") is not None
        assert schedule.get("period") is not None
        assert schedule.get("weekdays") is True
        assert schedule.get("route") is not None
        assert schedule.get("time") <= "05:00:00"


@pytest.mark.asyncio
async def test_create_shuttle_timetable(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_route,
    create_test_shuttle_period,
):
    access_token = await get_access_token(client)
    response = await client.post(
        "/api/shuttle/timetable",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "period": "semester",
            "weekdays": True,
            "route": "test_route1",
            "time": "00:00:00",
        },
    )
    assert response.status_code == 201
    response_json = response.json()
    assert response_json.get("sequence") == 1
    assert response_json.get("period") == "semester"
    assert response_json.get("weekdays") is True
    assert response_json.get("route") == "test_route1"
    assert response_json.get("time") == "00:00:00"
    check_statement = select(ShuttleTimetable).where(
        ShuttleTimetable.period == "semester",
        ShuttleTimetable.route_name == "test_route1",
    )
    query_result = await fetch_one(check_statement)
    assert query_result is not None


@pytest.mark.asyncio
async def test_create_shuttle_timetable_duplicate(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_timetable,
):
    access_token = await get_access_token(client)
    response = await client.post(
        "/api/shuttle/timetable",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "period": "semester",
            "weekdays": True,
            "route": "test_route1",
            "time": "01:00:00",
        },
    )
    assert response.status_code == 409
    response_json = response.json()
    assert response_json.get("detail") == "DUPLICATE_TIMETABLE"


@pytest.mark.asyncio
async def test_create_shuttle_timetable_route_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_timetable,
):
    access_token = await get_access_token(client)
    response = await client.post(
        "/api/shuttle/timetable",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "period": "semester",
            "weekdays": True,
            "route": "test_route100",
            "time": "01:00:00",
        },
    )
    assert response.status_code == 404
    response_json = response.json()
    assert response_json.get("detail") == "ROUTE_NOT_FOUND"


@pytest.mark.asyncio
async def test_create_shuttle_timetable_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_route,
    create_test_shuttle_period,
    monkeypatch: pytest.MonkeyPatch,
):
    from shuttle import service

    async def mock_create_timetable(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "create_timetable", mock_create_timetable)

    access_token = await get_access_token(client)
    response = await client.post(
        "/api/shuttle/timetable",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "period": "semester",
            "weekdays": True,
            "route": "test_route1",
            "time": "00:00:00",
        },
    )
    assert response.status_code == 500
    response_json = response.json()
    assert response_json.get("detail") == "INTERNAL_SERVER_ERROR"


@pytest.mark.asyncio
async def test_get_shuttle_timetable_item(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_timetable,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/shuttle/timetable/1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("sequence") is not None
    assert response_json.get("period") is not None
    assert response_json.get("weekdays") is not None
    assert response_json.get("route") is not None
    assert response_json.get("time") is not None


@pytest.mark.asyncio
async def test_get_shuttle_timetable_item_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_timetable,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/shuttle/timetable/1000",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    response_json = response.json()
    assert response_json.get("detail") == "TIMETABLE_NOT_FOUND"


@pytest.mark.asyncio
async def test_update_shuttle_timetable_item(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_timetable,
):
    access_token = await get_access_token(client)
    response = await client.patch(
        "/api/shuttle/timetable/1",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "period": "semester",
            "weekdays": True,
            "route": "test_route1",
            "time": "00:00:00",
        },
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("sequence") is not None
    assert response_json.get("period") is not None
    assert response_json.get("weekdays") is not None
    assert response_json.get("route") is not None
    assert response_json.get("time") is not None


@pytest.mark.asyncio
async def test_update_shuttle_timetable_item_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_timetable,
):
    access_token = await get_access_token(client)
    response = await client.patch(
        "/api/shuttle/timetable/1000",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "period": "semester",
            "weekdays": True,
            "route": "test_route1",
            "time": "00:00:00",
        },
    )
    assert response.status_code == 404
    response_json = response.json()
    assert response_json.get("detail") == "TIMETABLE_NOT_FOUND"


@pytest.mark.asyncio
async def test_update_shuttle_timetable_item_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_timetable,
    monkeypatch: pytest.MonkeyPatch,
):
    from shuttle import service

    async def mock_update_timetable(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "update_timetable", mock_update_timetable)

    access_token = await get_access_token(client)
    response = await client.patch(
        "/api/shuttle/timetable/1",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "period": "semester",
            "weekdays": True,
            "route": "test_route1",
            "time": "00:00:00",
        },
    )
    assert response.status_code == 500
    response_json = response.json()
    assert response_json.get("detail") == "INTERNAL_SERVER_ERROR"


@pytest.mark.asyncio
async def test_delete_shuttle_timetable_item(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_timetable,
):
    access_token = await get_access_token(client)
    response = await client.delete(
        "/api/shuttle/timetable/1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_shuttle_timetable_item_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_timetable,
):
    access_token = await get_access_token(client)
    response = await client.delete(
        "/api/shuttle/timetable/1000",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    response_json = response.json()
    assert response_json.get("detail") == "TIMETABLE_NOT_FOUND"


@pytest.mark.asyncio
async def test_get_shuttle_timetable_view(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_timetable,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/shuttle/timetable-view",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json.get("data")) >= 0
    for schedule in response_json.get("data"):
        assert schedule.get("sequence") is not None
        assert schedule.get("period") is not None
        assert schedule.get("weekdays") is not None
        assert schedule.get("route") is not None
        assert schedule.get("stop") is not None
        assert schedule.get("time") is not None


@pytest.mark.asyncio
async def test_get_shuttle_timetable_view_filter_route(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_timetable,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/shuttle/timetable-view?route=test_route1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    for schedule in response_json.get("data"):
        assert schedule.get("sequence") is not None
        assert schedule.get("period") is not None
        assert schedule.get("weekdays") is not None
        assert schedule.get("route") == "test_route1"
        assert schedule.get("stop") is not None
        assert schedule.get("time") is not None


@pytest.mark.asyncio
async def test_get_shuttle_timetable_view_filter_stop(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_timetable,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/shuttle/timetable-view?stop=test_stop1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    for schedule in response_json.get("data"):
        assert schedule.get("sequence") is not None
        assert schedule.get("period") is not None
        assert schedule.get("weekdays") is not None
        assert schedule.get("route") is not None
        assert schedule.get("stop") == "test_stop1"
        assert schedule.get("time") is not None


@pytest.mark.asyncio
async def test_get_shuttle_timetable_view_filter_period(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_timetable,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/shuttle/timetable-view?period=semester",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    for schedule in response_json.get("data"):
        assert schedule.get("sequence") is not None
        assert schedule.get("period") == "semester"
        assert schedule.get("weekdays") is not None
        assert schedule.get("route") is not None
        assert schedule.get("stop") is not None
        assert schedule.get("time") is not None


@pytest.mark.asyncio
async def test_get_shuttle_timetable_view_filter_weekdays(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_timetable,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/shuttle/timetable-view?weekdays=true",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    for schedule in response_json.get("data"):
        assert schedule.get("sequence") is not None
        assert schedule.get("period") is not None
        assert schedule.get("weekdays") is True
        assert schedule.get("route") is not None
        assert schedule.get("stop") is not None
        assert schedule.get("time") is not None

    response = await client.get(
        "/api/shuttle/timetable-view?weekdays=false",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    for schedule in response_json.get("data"):
        assert schedule.get("sequence") is not None
        assert schedule.get("period") is not None
        assert schedule.get("weekdays") is False
        assert schedule.get("route") is not None
        assert schedule.get("stop") is not None
        assert schedule.get("time") is not None


@pytest.mark.asyncio
async def test_get_shuttle_timetable_view_filter_start_time(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_timetable,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/shuttle/timetable-view?start=00:00",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    for schedule in response_json.get("data"):
        assert schedule.get("sequence") is not None
        assert schedule.get("period") is not None
        assert schedule.get("weekdays") is True
        assert schedule.get("route") is not None
        assert schedule.get("stop") is not None
        assert schedule.get("time") >= "00:00"


@pytest.mark.asyncio
async def test_get_shuttle_timetable_view_filter_end_time(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_shuttle_timetable,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/shuttle/timetable-view?end=05:00",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()

    for schedule in response_json.get("data"):
        assert schedule.get("sequence") is not None
        assert schedule.get("period") is not None
        assert schedule.get("weekdays") is True
        assert schedule.get("route") is not None
        assert schedule.get("stop") is not None
        assert schedule.get("time") <= "05:00"
