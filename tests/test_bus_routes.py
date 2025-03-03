from datetime import time

import pytest
from async_asgi_testclient import TestClient
from sqlalchemy import select

from database import fetch_one
from model.bus import BusRoute, BusStop, BusRouteStop, BusTimetable
from tests.utils import get_access_token
from utils import KST


@pytest.mark.asyncio
async def test_bus_routes(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_route,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/bus/route",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json.get("data")) > 0
    for route in response_json.get("data"):
        assert route.get("id") is not None
        assert route.get("name") is not None
        assert route.get("type") is not None


@pytest.mark.asyncio
async def test_bus_routes_filter_name(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_route,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/bus/route?name=test_route",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json.get("data")) > 0
    for route in response_json.get("data"):
        assert route.get("id") is not None
        assert "test_route" in route.get("name")
        assert route.get("type") is not None


@pytest.mark.asyncio
async def test_bus_routes_filter_type(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_route,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/bus/route?type_=EXPRESS",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json.get("data")) > 0
    for route in response_json.get("data"):
        assert route.get("id") is not None
        assert route.get("name") is not None
        assert route.get("type") == "EXPRESS"


@pytest.mark.asyncio
async def test_bus_routes_filter_company(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_route,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/bus/route?company=test_company",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json.get("data")) > 0
    for route in response_json.get("data"):
        assert route.get("id") is not None
        assert route.get("name") is not None
        assert route.get("type") is not None


@pytest.mark.asyncio
async def test_bus_route_detail(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_route,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/bus/route/1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("id") is not None
    assert response_json.get("name") is not None
    assert response_json.get("type") is not None
    assert response_json.get("company") is not None
    assert response_json.get("start") is not None
    assert response_json.get("end") is not None
    assert response_json.get("company") is not None
    assert response_json["company"].get("id") is not None
    assert response_json["company"].get("name") is not None
    assert response_json["company"].get("telephone") is not None
    assert response_json.get("up") is not None
    assert response_json["up"].get("first") is not None
    assert response_json["up"].get("last") is not None
    assert response_json.get("down") is not None
    assert response_json["down"].get("first") is not None
    assert response_json["down"].get("last") is not None


@pytest.mark.asyncio
async def test_bus_route_detail_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_route,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/bus/route/20",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "ROUTE_NOT_FOUND"}


@pytest.mark.asyncio
async def test_create_bus_route(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_route,
):
    access_token = await get_access_token(client)
    new_route = {
        "id": 20,
        "name": "test_route",
        "typeCode": "11",
        "typeName": "일반형시내버스",
        "start": 1,
        "end": 9,
        "upFirstTime": "06:00:00",
        "upLastTime": "23:00:00",
        "downFirstTime": "06:00:00",
        "downLastTime": "23:00:00",
        "companyID": 1,
        "companyName": "test_company",
        "companyTelephone": "010-1234-5678",
        "district": 1,
    }
    response = await client.post(
        "/api/bus/route",
        json=new_route,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 201
    response_json = response.json()
    assert response_json.get("id") is not None
    assert response_json.get("name") is not None
    assert response_json.get("type") is not None
    assert response_json.get("company") is not None
    assert response_json.get("start") is not None
    assert response_json.get("end") is not None
    assert response_json.get("company") is not None
    assert response_json["company"].get("id") is not None
    assert response_json["company"].get("name") is not None
    assert response_json["company"].get("telephone") is not None
    assert response_json.get("up") is not None
    assert response_json["up"].get("first") is not None
    assert response_json["up"].get("last") is not None
    assert response_json.get("down") is not None
    assert response_json["down"].get("first") is not None
    assert response_json["down"].get("last") is not None
    check_statement = select(BusRoute).where(BusRoute.id_ == 20)
    query_result = await fetch_one(check_statement)
    assert query_result is not None
    assert query_result.name == "test_route"


@pytest.mark.asyncio
async def test_create_bus_route_duplicate_id(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_route,
):
    access_token = await get_access_token(client)
    new_route = {
        "id": 1,
        "name": "test_route",
        "typeCode": "11",
        "typeName": "일반형시내버스",
        "start": 1,
        "end": 9,
        "upFirstTime": "06:00:00",
        "upLastTime": "23:00:00",
        "downFirstTime": "06:00:00",
        "downLastTime": "23:00:00",
        "companyID": 1,
        "companyName": "test_company",
        "companyTelephone": "010-1234-5678",
        "district": 1,
    }
    response = await client.post(
        "/api/bus/route",
        json=new_route,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "DUPLICATE_ROUTE_ID"}


@pytest.mark.asyncio
async def test_create_bus_route_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_route,
    monkeypatch: pytest.MonkeyPatch,
):
    from bus import service

    async def mock_create_route(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "create_route", mock_create_route)
    access_token = await get_access_token(client)
    new_route = {
        "id": 20,
        "name": "test_route",
        "typeCode": "11",
        "typeName": "일반형시내버스",
        "start": 1,
        "end": 9,
        "upFirstTime": "06:00:00",
        "upLastTime": "23:00:00",
        "downFirstTime": "06:00:00",
        "downLastTime": "23:00:00",
        "companyID": 1,
        "companyName": "test_company",
        "companyTelephone": "010-1234-5678",
        "district": 1,
    }
    response = await client.post(
        "/api/bus/route",
        json=new_route,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 500
    assert response.json() == {"detail": "INTERNAL_SERVER_ERROR"}


@pytest.mark.asyncio
async def test_update_bus_route(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_route,
):
    access_token = await get_access_token(client)
    update_route = {
        "name": "test_route",
        "typeCode": "11",
        "typeName": "일반형시내버스",
        "start": 1,
        "end": 9,
        "upFirstTime": "06:00:00",
        "upLastTime": "23:00:00",
        "downFirstTime": "06:00:00",
        "downLastTime": "23:00:00",
        "companyID": 1,
        "companyName": "test_company",
        "companyTelephone": "010-1234-5678",
        "district": 1,
    }
    response = await client.patch(
        "/api/bus/route/1",
        json=update_route,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("id") is not None
    assert response_json.get("name") is not None
    assert response_json.get("type") is not None
    assert response_json.get("company") is not None
    assert response_json.get("start") is not None
    assert response_json.get("end") is not None
    assert response_json.get("company") is not None
    assert response_json["company"].get("id") is not None
    assert response_json["company"].get("name") is not None
    assert response_json["company"].get("telephone") is not None
    assert response_json.get("up") is not None
    assert response_json["up"].get("first") is not None
    assert response_json["up"].get("last") is not None
    assert response_json.get("down") is not None
    assert response_json["down"].get("first") is not None
    assert response_json["down"].get("last") is not None


@pytest.mark.asyncio
async def test_update_bus_route_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_route,
):
    access_token = await get_access_token(client)
    update_route = {
        "name": "test_route",
        "typeCode": "11",
        "typeName": "일반형시내버스",
        "start": 1,
        "end": 9,
        "upFirstTime": "06:00:00",
        "upLastTime": "23:00:00",
        "downFirstTime": "06:00:00",
        "downLastTime": "23:00:00",
        "companyID": 1,
        "companyName": "test_company",
        "companyTelephone": "010-1234-5678",
        "district": 1,
    }
    response = await client.patch(
        "/api/bus/route/20",
        json=update_route,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "ROUTE_NOT_FOUND"}


@pytest.mark.asyncio
async def test_update_bus_route_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_route,
    monkeypatch: pytest.MonkeyPatch,
):
    from bus import service

    async def mock_update_route(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "update_route", mock_update_route)
    access_token = await get_access_token(client)
    update_route = {
        "name": "test_route",
        "typeCode": "11",
        "typeName": "일반형시내버스",
        "start": 1,
        "end": 9,
        "upFirstTime": "06:00:00",
        "upLastTime": "23:00:00",
        "downFirstTime": "06:00:00",
        "downLastTime": "23:00:00",
        "companyID": 1,
        "companyName": "test_company",
        "companyTelephone": "010-1234-5678",
        "district": 1,
    }
    response = await client.patch(
        "/api/bus/route/1",
        json=update_route,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 500
    assert response.json() == {"detail": "INTERNAL_SERVER_ERROR"}


@pytest.mark.asyncio
async def test_delete_bus_route(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_route,
):
    access_token = await get_access_token(client)
    response = await client.delete(
        "/api/bus/route/1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_bus_route_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_route,
):
    access_token = await get_access_token(client)
    response = await client.delete(
        "/api/bus/route/20",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "ROUTE_NOT_FOUND"}


@pytest.mark.asyncio
async def test_stop_list(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_stop,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/bus/stop",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json.get("data")) > 0
    for stop in response_json.get("data"):
        assert stop.get("id") is not None
        assert stop.get("name") is not None


@pytest.mark.asyncio
async def test_stop_list_filter_name(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_stop,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/bus/stop?name=test_stop",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json.get("data")) > 0
    for stop in response_json.get("data"):
        assert stop.get("id") is not None
        assert "test_stop" in stop.get("name")


@pytest.mark.asyncio
async def test_stop_detail(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_stop,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/bus/stop/1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("id") is not None
    assert response_json.get("name") is not None
    assert response_json.get("latitude") is not None
    assert response_json.get("longitude") is not None
    assert response_json.get("district") is not None
    assert response_json.get("mobileNumber") is not None
    assert response_json.get("regionName") is not None


@pytest.mark.asyncio
async def test_stop_detail_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_stop,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/bus/stop/20",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "STOP_NOT_FOUND"}


@pytest.mark.asyncio
async def test_create_bus_stop(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_stop,
):
    access_token = await get_access_token(client)
    new_stop = {
        "id": 20,
        "name": "test_stop",
        "latitude": 37.123456,
        "longitude": 127.123456,
        "district": 1,
        "mobileNumber": "01090",
        "regionName": "test",
    }
    response = await client.post(
        "/api/bus/stop",
        json=new_stop,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 201
    response_json = response.json()
    assert response_json.get("id") is not None
    assert response_json.get("name") is not None
    assert response_json.get("latitude") is not None
    assert response_json.get("longitude") is not None
    assert response_json.get("district") is not None
    assert response_json.get("mobileNumber") is not None
    assert response_json.get("regionName") is not None
    check_statement = select(BusStop).where(BusStop.id_ == 20)
    query_result = await fetch_one(check_statement)
    assert query_result is not None
    assert query_result.name == "test_stop"


@pytest.mark.asyncio
async def test_create_bus_stop_duplicate_id(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_stop,
):
    access_token = await get_access_token(client)
    new_stop = {
        "id": 1,
        "name": "test_stop",
        "latitude": 37.123456,
        "longitude": 127.123456,
        "district": 1,
        "mobileNumber": "01090",
        "regionName": "test",
    }
    response = await client.post(
        "/api/bus/stop",
        json=new_stop,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "DUPLICATE_STOP_ID"}


@pytest.mark.asyncio
async def test_create_bus_stop_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_stop,
    monkeypatch: pytest.MonkeyPatch,
):
    from bus import service

    async def mock_create_stop(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "create_stop", mock_create_stop)
    access_token = await get_access_token(client)
    new_stop = {
        "id": 20,
        "name": "test_stop",
        "latitude": 37.123456,
        "longitude": 127.123456,
        "district": 1,
        "mobileNumber": "01090",
        "regionName": "test",
    }
    response = await client.post(
        "/api/bus/stop",
        json=new_stop,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 500
    assert response.json() == {"detail": "INTERNAL_SERVER_ERROR"}


@pytest.mark.asyncio
async def test_update_bus_stop(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_stop,
):
    access_token = await get_access_token(client)
    update_stop = {
        "name": "test_stop",
        "latitude": 37.123456,
        "longitude": 127.123456,
        "district": 1,
        "mobileNumber": "01090",
        "regionName": "test",
    }
    response = await client.patch(
        "/api/bus/stop/1",
        json=update_stop,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("id") is not None
    assert response_json.get("name") is not None
    assert response_json.get("latitude") is not None
    assert response_json.get("longitude") is not None
    assert response_json.get("district") is not None
    assert response_json.get("mobileNumber") is not None
    assert response_json.get("regionName") is not None


@pytest.mark.asyncio
async def test_update_bus_stop_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_stop,
):
    access_token = await get_access_token(client)
    update_stop = {
        "name": "test_stop",
        "latitude": 37.123456,
        "longitude": 127.123456,
        "district": 1,
        "mobileNumber": "01090",
        "regionName": "test",
    }
    response = await client.patch(
        "/api/bus/stop/20",
        json=update_stop,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "STOP_NOT_FOUND"}


@pytest.mark.asyncio
async def test_update_bus_stop_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_stop,
    monkeypatch: pytest.MonkeyPatch,
):
    from bus import service

    async def mock_update_stop(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "update_stop", mock_update_stop)
    access_token = await get_access_token(client)
    update_stop = {
        "name": "test_stop",
        "latitude": 37.123456,
        "longitude": 127.123456,
        "district": 1,
        "mobileNumber": "01090",
        "regionName": "test",
    }
    response = await client.patch(
        "/api/bus/stop/1",
        json=update_stop,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 500
    assert response.json() == {"detail": "INTERNAL_SERVER_ERROR"}


@pytest.mark.asyncio
async def test_delete_bus_stop(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_stop,
):
    access_token = await get_access_token(client)
    response = await client.delete(
        "/api/bus/stop/1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_bus_stop_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_stop,
):
    access_token = await get_access_token(client)
    response = await client.delete(
        "/api/bus/stop/20",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "STOP_NOT_FOUND"}


@pytest.mark.asyncio
async def test_bus_route_stop_list(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_route_stop,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/bus/route-stop",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert len(response.json().get("data")) > 0
    for stop in response.json().get("data"):
        assert stop.get("id") is not None
        assert stop.get("sequence") is not None
        assert stop.get("start") is not None
        assert stop.get("minuteFromStart") is not None


@pytest.mark.asyncio
async def test_bus_route_stop_list_filter(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_route_stop,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/bus/route/1/stop",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert len(response.json().get("data")) > 0
    for stop in response.json().get("data"):
        assert stop.get("id") is not None
        assert stop.get("sequence") is not None
        assert stop.get("start") is not None
        assert stop.get("minuteFromStart") is not None


@pytest.mark.asyncio
async def test_bus_route_stop_list_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_route_stop,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/bus/route/20/stop",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "ROUTE_NOT_FOUND"}


@pytest.mark.asyncio
async def test_bus_route_stop_detail(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_route_stop,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/bus/route/1/stop/1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert response.json().get("id") is not None
    assert response.json().get("sequence") is not None
    assert response.json().get("start") is not None
    assert response.json().get("minuteFromStart") is not None


@pytest.mark.asyncio
async def test_bus_route_stop_detail_not_found_route(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_route_stop,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/bus/route/20/stop/1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "ROUTE_NOT_FOUND"}


@pytest.mark.asyncio
async def test_bus_route_stop_detail_not_found_stop(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_route_stop,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/bus/route/1/stop/20",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "STOP_NOT_FOUND"}


@pytest.mark.asyncio
async def test_bus_route_stop_detail_not_found_route_stop(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_route_stop,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/bus/route/1/stop/9",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "ROUTE_STOP_NOT_FOUND"}


@pytest.mark.asyncio
async def test_create_bus_route_stop(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_route_stop,
):
    access_token = await get_access_token(client)
    new_route_stop = {
        "routeID": 1,
        "stopID": 9,
        "sequence": 1,
        "start": 1,
        "minuteFromStart": 1,
    }
    response = await client.post(
        "/api/bus/route/1/stop",
        json=new_route_stop,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 201
    assert response.json().get("id") is not None
    assert response.json().get("sequence") is not None
    assert response.json().get("start") is not None
    assert response.json().get("minuteFromStart") is not None
    check_statement = select(BusRouteStop).where(
        BusRouteStop.route_id == 1, BusRouteStop.stop_id == 9
    )
    query_result = await fetch_one(check_statement)
    assert query_result is not None
    assert query_result.sequence == 1


@pytest.mark.asyncio
async def test_create_bus_route_stop_duplicate(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_route_stop,
):
    access_token = await get_access_token(client)
    new_route_stop = {
        "routeID": 1,
        "stopID": 7,
        "sequence": 1,
        "start": 1,
        "minuteFromStart": 1,
    }
    response = await client.post(
        "/api/bus/route/1/stop",
        json=new_route_stop,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "DUPLICATE_ROUTE_STOP"}


@pytest.mark.asyncio
async def test_create_bus_route_stop_not_found_route(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_route_stop,
):
    access_token = await get_access_token(client)
    new_route_stop = {
        "routeID": 20,
        "stopID": 9,
        "sequence": 1,
        "start": 1,
        "minuteFromStart": 1,
    }
    response = await client.post(
        "/api/bus/route/20/stop",
        json=new_route_stop,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "ROUTE_NOT_FOUND"}


@pytest.mark.asyncio
async def test_create_bus_route_stop_not_found_stop(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_route_stop,
):
    access_token = await get_access_token(client)
    new_route_stop = {
        "routeID": 1,
        "stopID": 20,
        "sequence": 1,
        "start": 1,
        "minuteFromStart": 1,
    }
    response = await client.post(
        "/api/bus/route/1/stop",
        json=new_route_stop,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "STOP_NOT_FOUND"}


@pytest.mark.asyncio
async def test_create_bus_route_stop_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_route_stop,
    monkeypatch: pytest.MonkeyPatch,
):
    from bus import service

    async def mock_create_route_stop(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "create_route_stop", mock_create_route_stop)
    access_token = await get_access_token(client)
    new_route_stop = {
        "routeID": 1,
        "stopID": 9,
        "sequence": 1,
        "start": 1,
        "minuteFromStart": 1,
    }
    response = await client.post(
        "/api/bus/route/1/stop",
        json=new_route_stop,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 500
    assert response.json() == {"detail": "INTERNAL_SERVER_ERROR"}


@pytest.mark.asyncio
async def test_update_bus_route_stop(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_route_stop,
):
    access_token = await get_access_token(client)
    update_route_stop = {
        "sequence": 1,
        "start": 1,
        "minuteFromStart": 1,
    }
    response = await client.patch(
        "/api/bus/route/1/stop/1",
        json=update_route_stop,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert response.json().get("id") is not None
    assert response.json().get("sequence") is not None
    assert response.json().get("start") is not None
    assert response.json().get("minuteFromStart") is not None


@pytest.mark.asyncio
async def test_update_bus_route_stop_not_found_route(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_route_stop,
):
    access_token = await get_access_token(client)
    update_route_stop = {
        "sequence": 1,
        "start": 1,
        "minuteFromStart": 1,
    }
    response = await client.patch(
        "/api/bus/route/20/stop/1",
        json=update_route_stop,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "ROUTE_NOT_FOUND"}


@pytest.mark.asyncio
async def test_update_bus_route_stop_not_found_stop(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_route_stop,
):
    access_token = await get_access_token(client)
    update_route_stop = {
        "sequence": 1,
        "start": 1,
        "minuteFromStart": 1,
    }
    response = await client.patch(
        "/api/bus/route/1/stop/20",
        json=update_route_stop,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "STOP_NOT_FOUND"}


@pytest.mark.asyncio
async def test_update_bus_route_stop_not_found_route_stop(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_route_stop,
):
    access_token = await get_access_token(client)
    update_route_stop = {
        "sequence": 1,
        "start": 1,
        "minuteFromStart": 1,
    }
    response = await client.patch(
        "/api/bus/route/1/stop/9",
        json=update_route_stop,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "ROUTE_STOP_NOT_FOUND"}


@pytest.mark.asyncio
async def test_delete_bus_route_stop(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_route_stop,
):
    access_token = await get_access_token(client)
    response = await client.delete(
        "/api/bus/route/1/stop/1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_bus_route_stop_not_found_route(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_route_stop,
):
    access_token = await get_access_token(client)
    response = await client.delete(
        "/api/bus/route/20/stop/1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "ROUTE_NOT_FOUND"}


@pytest.mark.asyncio
async def test_delete_bus_route_stop_not_found_stop(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_route_stop,
):
    access_token = await get_access_token(client)
    response = await client.delete(
        "/api/bus/route/1/stop/20",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "STOP_NOT_FOUND"}


@pytest.mark.asyncio
async def test_delete_bus_route_stop_not_found_route_stop(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_route_stop,
):
    access_token = await get_access_token(client)
    response = await client.delete(
        "/api/bus/route/1/stop/9",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "ROUTE_STOP_NOT_FOUND"}


@pytest.mark.asyncio
async def test_list_timetable(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_timetable,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/bus/timetable",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert len(response.json().get("data")) > 0
    for timetable in response.json().get("data"):
        assert timetable.get("routeID") is not None
        assert timetable.get("start") is not None
        assert timetable.get("weekdays") is not None
        assert timetable.get("departureTime") is not None


@pytest.mark.asyncio
async def test_list_timetable_start_stop_filter(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_timetable,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/bus/timetable?start_stop_id=1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert len(response.json().get("data")) > 0
    for timetable in response.json().get("data"):
        assert timetable.get("routeID") is not None
        assert timetable.get("start") is not None
        assert timetable.get("weekdays") is not None
        assert timetable.get("departureTime") is not None


@pytest.mark.asyncio
async def test_list_timetable_weekdays_filter(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_timetable,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/bus/timetable?weekdays=saturday",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert len(response.json().get("data")) > 0
    for timetable in response.json().get("data"):
        assert timetable.get("routeID") is not None
        assert timetable.get("start") is not None
        assert timetable.get("weekdays") == "saturday"
        assert timetable.get("departureTime") is not None


@pytest.mark.asyncio
async def test_list_timetable_route_filter(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_timetable,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/bus/timetable?route_id=1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert len(response.json().get("data")) > 0
    for timetable in response.json().get("data"):
        assert timetable.get("routeID") == 1
        assert timetable.get("start") is not None
        assert timetable.get("weekdays") is not None
        assert timetable.get("departureTime") is not None


@pytest.mark.asyncio
async def test_list_timetable_start_filter(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_timetable,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/bus/timetable?start=05:00:00",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert len(response.json().get("data")) > 0
    for timetable in response.json().get("data"):
        assert timetable.get("routeID") is not None
        assert timetable.get("start") == 1
        assert timetable.get("weekdays") is not None
        assert timetable.get("departureTime") >= "05:00:00"


@pytest.mark.asyncio
async def test_list_timetable_end_filter(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_timetable,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/bus/timetable?end=05:00:00",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert len(response.json().get("data")) > 0
    for timetable in response.json().get("data"):
        assert timetable.get("routeID") is not None
        assert timetable.get("start") is not None
        assert timetable.get("weekdays") is not None
        assert timetable.get("departureTime") <= "05:00:00"


@pytest.mark.asyncio
async def test_get_timetable(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_timetable,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/bus/timetable/1/1/weekdays/05:00:00",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert response.json().get("routeID") is not None
    assert response.json().get("start") is not None
    assert response.json().get("weekdays") == "weekdays"
    assert response.json().get("departureTime") == "05:00:00"


@pytest.mark.asyncio
async def test_get_timetable_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_timetable,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/bus/timetable/1/1/weekdays/15:00:00",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "TIMETABLE_NOT_FOUND"}


@pytest.mark.asyncio
async def test_get_timetable_route_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_timetable,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/bus/timetable/20/1/weekdays/05:00:00",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "ROUTE_NOT_FOUND"}


@pytest.mark.asyncio
async def test_get_timetable_stop_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_timetable,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/bus/timetable/1/20/weekdays/05:00:00",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "STOP_NOT_FOUND"}


@pytest.mark.asyncio
async def test_create_timetable(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_timetable,
):
    access_token = await get_access_token(client)
    new_timetable = {
        "routeID": 1,
        "start": 1,
        "weekdays": "saturday",
        "departureTime": "15:00:00",
    }
    response = await client.post(
        "/api/bus/timetable",
        json=new_timetable,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 201
    assert response.json().get("routeID") is not None
    assert response.json().get("start") is not None
    assert response.json().get("weekdays") is not None
    assert response.json().get("departureTime") is not None
    check_statement = select(BusTimetable).where(
        BusTimetable.route_id == 1,
        BusTimetable.start_stop_id == 1,
        BusTimetable.weekday == "saturday",
        BusTimetable.departure_time == time(hour=15).replace(tzinfo=KST),
    )
    query_result = await fetch_one(check_statement)
    assert query_result is not None


@pytest.mark.asyncio
async def test_create_timetable_duplicate(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_timetable,
):
    access_token = await get_access_token(client)
    new_timetable = {
        "routeID": 1,
        "start": 1,
        "weekdays": "weekdays",
        "departureTime": "05:00:00",
    }
    response = await client.post(
        "/api/bus/timetable",
        json=new_timetable,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "DUPLICATE_TIMETABLE"}


@pytest.mark.asyncio
async def test_create_timetable_route_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_timetable,
):
    access_token = await get_access_token(client)
    new_timetable = {
        "routeID": 20,
        "start": 1,
        "weekdays": "saturday",
        "departureTime": "15:00:00",
    }
    response = await client.post(
        "/api/bus/timetable",
        json=new_timetable,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "ROUTE_NOT_FOUND"}


@pytest.mark.asyncio
async def test_create_timetable_start_stop_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_timetable,
):
    access_token = await get_access_token(client)
    new_timetable = {
        "routeID": 1,
        "start": 20,
        "weekdays": "saturday",
        "departureTime": "15:00:00",
    }
    response = await client.post(
        "/api/bus/timetable",
        json=new_timetable,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "START_STOP_NOT_FOUND"}


@pytest.mark.asyncio
async def test_create_timetable_internal_server_error(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_timetable,
    monkeypatch: pytest.MonkeyPatch,
):
    from bus import service

    async def mock_create_timetable(*args, **kwargs):
        return None

    monkeypatch.setattr(service, "create_timetable", mock_create_timetable)
    access_token = await get_access_token(client)
    new_timetable = {
        "routeID": 1,
        "start": 1,
        "weekdays": "saturday",
        "departureTime": "15:00:00",
    }
    response = await client.post(
        "/api/bus/timetable",
        json=new_timetable,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 500
    assert response.json() == {"detail": "INTERNAL_SERVER_ERROR"}


@pytest.mark.asyncio
async def test_delete_timetable(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_timetable,
):
    access_token = await get_access_token(client)
    response = await client.delete(
        "/api/bus/timetable/1/1/weekdays/05:00:00",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_timetable_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_timetable,
):
    access_token = await get_access_token(client)
    response = await client.delete(
        "/api/bus/timetable/1/1/saturday/15:00:00",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "TIMETABLE_NOT_FOUND"}


@pytest.mark.asyncio
async def test_delete_timetable_route_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_timetable,
):
    access_token = await get_access_token(client)
    response = await client.delete(
        "/api/bus/timetable/20/1/saturday/05:00:00",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "ROUTE_NOT_FOUND"}


@pytest.mark.asyncio
async def test_delete_timetable_stop_not_found(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_timetable,
):
    access_token = await get_access_token(client)
    response = await client.delete(
        "/api/bus/timetable/1/20/saturday/05:00:00",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "STOP_NOT_FOUND"}


@pytest.mark.asyncio
async def test_list_realtime(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_realtime,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/bus/realtime",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert len(response.json().get("data")) > 0
    for realtime in response.json().get("data"):
        assert realtime.get("routeID") is not None
        assert realtime.get("stopID") is not None
        assert realtime.get("sequence") is not None
        assert realtime.get("stop") is not None
        assert realtime.get("seat") is not None
        assert realtime.get("time") is not None
        assert realtime.get("lowFloor") is not None
        assert realtime.get("updatedAt") is not None


@pytest.mark.asyncio
async def test_list_realtime_stop_filter(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_realtime,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/bus/realtime?stop_id=1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert len(response.json().get("data")) > 0
    for realtime in response.json().get("data"):
        assert realtime.get("routeID") is not None
        assert realtime.get("stopID") == 1
        assert realtime.get("sequence") is not None
        assert realtime.get("stop") is not None
        assert realtime.get("seat") is not None
        assert realtime.get("time") is not None
        assert realtime.get("lowFloor") is not None
        assert realtime.get("updatedAt") is not None


@pytest.mark.asyncio
async def test_list_realtime_route_filter(
    client: TestClient,
    clean_db,
    create_test_user,
    create_test_bus_realtime,
):
    access_token = await get_access_token(client)
    response = await client.get(
        "/api/bus/realtime?route_id=1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert len(response.json().get("data")) > 0
    for realtime in response.json().get("data"):
        assert realtime.get("routeID") == 1
        assert realtime.get("stopID") is not None
        assert realtime.get("sequence") is not None
        assert realtime.get("stop") is not None
        assert realtime.get("seat") is not None
        assert realtime.get("time") is not None
        assert realtime.get("lowFloor") is not None
        assert realtime.get("updatedAt") is not None
