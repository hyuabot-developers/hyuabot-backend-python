import pytest
from async_asgi_testclient import TestClient

from query.router import graphql_schema


def validate_response(response: dict) -> None:
    assert isinstance(response["id"], int)
    assert isinstance(response["name"], str)
    assert isinstance(response["districtCode"], int)
    assert isinstance(response["region"], str)
    assert isinstance(response["mobileNumber"], str)
    assert isinstance(response["latitude"], float)
    assert isinstance(response["longitude"], float)
    assert isinstance(response["routes"], list)
    routes = response["routes"]
    for route in routes:
        assert isinstance(route["minuteFromStart"], int)
        assert isinstance(route["sequence"], int)
        assert isinstance(route["info"], dict)
        assert isinstance(route["timetable"], list)
        assert isinstance(route["realtime"], list)
        route_info = route["info"]
        assert isinstance(route_info["id"], int)
        assert isinstance(route_info["name"], str)
        assert isinstance(route_info["type"], dict)
        assert isinstance(route_info["start"], dict)
        assert isinstance(route_info["end"], dict)
        assert isinstance(route_info["runningTime"], dict)
        company = route_info["company"]
        route_type = route_info["type"]
        start_stop = route_info["start"]
        end_stop = route_info["end"]
        running_time = route_info["runningTime"]
        assert isinstance(company["id"], int)
        assert isinstance(company["name"], str)
        assert isinstance(company["telephone"], str)
        assert isinstance(route_type["code"], str)
        assert isinstance(route_type["name"], str)
        assert isinstance(start_stop["id"], int)
        assert isinstance(start_stop["name"], str)
        assert isinstance(start_stop["districtCode"], int)
        assert isinstance(start_stop["region"], str)
        assert isinstance(start_stop["mobileNumber"], str)
        assert isinstance(start_stop["latitude"], float)
        assert isinstance(start_stop["longitude"], float)
        assert isinstance(end_stop["id"], int)
        assert isinstance(end_stop["name"], str)
        assert isinstance(end_stop["districtCode"], int)
        assert isinstance(end_stop["region"], str)
        assert isinstance(end_stop["mobileNumber"], str)
        assert isinstance(end_stop["latitude"], float)
        assert isinstance(end_stop["longitude"], float)
        assert isinstance(running_time["up"], dict)
        assert isinstance(running_time["down"], dict)
        up_running_time = running_time["up"]
        down_running_time = running_time["down"]
        assert isinstance(up_running_time["first"], str)
        assert isinstance(up_running_time["last"], str)
        assert isinstance(down_running_time["first"], str)
        assert isinstance(down_running_time["last"], str)
        for item in route["timetable"]:
            assert isinstance(item["weekdays"], str)
            assert isinstance(item["time"], str)
        for item in route["realtime"]:
            assert isinstance(item["sequence"], int)
            assert isinstance(item["stop"], int)
            assert isinstance(item["time"], float)
            assert isinstance(item["seat"], int)
            assert isinstance(item["lowFloor"], bool)
            assert isinstance(item["updatedAt"], str)
        for item in route["log"]:
            assert isinstance(item["departureDate"], str)
            assert isinstance(item["departureTime"], str)
            assert isinstance(item["vehicleId"], str)


@pytest.mark.asyncio
async def test_get_bus_query(
    client: TestClient,
    clean_db,
    create_test_bus_realtime,
    create_test_bus_timetable,
    create_test_bus_departure_log,
) -> None:
    query = """
        query {
            bus {
                id, name, districtCode, region, mobileNumber, latitude, longitude,
                routes {
                    sequence,
                    minuteFromStart,
                    info {
                        id, name,
                        company { id, name, telephone }, type { code, name },
                        start {
                            id, name, districtCode, region,
                            mobileNumber, latitude, longitude
                        },
                        end {
                            id, name, districtCode, region,
                            mobileNumber, latitude, longitude
                        },
                        runningTime { up { first, last }, down { first, last } }
                    }
                timetable { weekdays, time },
                realtime { sequence, stop, time, seat, lowFloor, updatedAt },
                log { departureDate, departureTime, vehicleId }
            }
        }
    }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["bus"], list)
    for stop in response.data["bus"]:
        validate_response(stop)


@pytest.mark.asyncio
async def test_get_bus_query_filter_stop_id(
    client: TestClient,
    clean_db,
    create_test_bus_realtime,
    create_test_bus_timetable,
) -> None:
    query = """
        query {
            bus (id_: [1]) {
                id, name, districtCode, region, mobileNumber, latitude, longitude,
                routes {
                    sequence,
                    minuteFromStart,
                    info {
                        id, name,
                        company { id, name, telephone }, type { code, name },
                        start {
                            id, name, districtCode, region,
                            mobileNumber, latitude, longitude
                        },
                        end {
                            id, name, districtCode, region,
                            mobileNumber, latitude, longitude
                        },
                        runningTime { up { first, last }, down { first, last } }
                    }
                timetable { weekdays, time },
                realtime { sequence, stop, time, seat, lowFloor, updatedAt },
                log { departureDate, departureTime, vehicleId }
            }
        }
    }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["bus"], list)
    for stop in response.data["bus"]:
        assert stop["id"] == 1
        validate_response(stop)


@pytest.mark.asyncio
async def test_get_bus_query_filter_stop_name(
    client: TestClient,
    clean_db,
    create_test_bus_realtime,
    create_test_bus_timetable,
) -> None:
    query = """
        query {
            bus (name: "test_stop") {
                id, name, districtCode, region, mobileNumber, latitude, longitude,
                routes {
                    sequence,
                    minuteFromStart,
                    info {
                        id, name,
                        company { id, name, telephone }, type { code, name },
                        start {
                            id, name, districtCode, region,
                            mobileNumber, latitude, longitude
                        },
                        end {
                            id, name, districtCode, region,
                            mobileNumber, latitude, longitude
                        },
                        runningTime { up { first, last }, down { first, last } }
                    }
                timetable { weekdays, time },
                realtime { sequence, stop, time, seat, lowFloor, updatedAt },
                log { departureDate, departureTime, vehicleId }
            }
        }
    }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["bus"], list)
    for stop in response.data["bus"]:
        assert "test_stop" in stop["name"]
        validate_response(stop)


@pytest.mark.asyncio
async def test_get_bus_query_filter_start_time(
    client: TestClient,
    clean_db,
    create_test_bus_realtime,
    create_test_bus_timetable,
) -> None:
    query = """
        query {
            bus (start: "00:05:00") {
                id, name, districtCode, region, mobileNumber, latitude, longitude,
                routes {
                    sequence,
                    minuteFromStart,
                    info {
                        id, name,
                        company { id, name, telephone }, type { code, name },
                        start {
                            id, name, districtCode, region,
                            mobileNumber, latitude, longitude
                        },
                        end {
                            id, name, districtCode, region,
                            mobileNumber, latitude, longitude
                        },
                        runningTime { up { first, last }, down { first, last } }
                    }
                timetable { weekdays, time },
                realtime { sequence, stop, time, seat, lowFloor, updatedAt },
                log { departureDate, departureTime, vehicleId }
            }
        }
    }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["bus"], list)
    for stop in response.data["bus"]:
        validate_response(stop)
        routes = stop["routes"]
        for route in routes:
            timetable = route["timetable"]
            for item in timetable:
                assert item["time"] >= "00:05:00"


@pytest.mark.asyncio
async def test_get_bus_query_filter_end_time(
    client: TestClient,
    clean_db,
    create_test_bus_realtime,
    create_test_bus_timetable,
) -> None:
    query = """
        query {
            bus (end: "00:05:00") {
                id, name, districtCode, region, mobileNumber, latitude, longitude,
                routes {
                    sequence,
                    minuteFromStart,
                    info {
                        id, name,
                        company { id, name, telephone }, type { code, name },
                        start {
                            id, name, districtCode, region,
                            mobileNumber, latitude, longitude
                        },
                        end {
                            id, name, districtCode, region,
                            mobileNumber, latitude, longitude
                        },
                        runningTime { up { first, last }, down { first, last } }
                    }
                timetable { weekdays, time },
                realtime { sequence, stop, time, seat, lowFloor, updatedAt },
                log { departureDate, departureTime, vehicleId }
            }
        }
    }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["bus"], list)
    for stop in response.data["bus"]:
        validate_response(stop)
        routes = stop["routes"]
        for route in routes:
            timetable = route["timetable"]
            for item in timetable:
                assert item["time"] <= "00:05:00"


@pytest.mark.asyncio
async def test_get_bus_query_filter_weekdays(
    client: TestClient,
    clean_db,
    create_test_bus_realtime,
    create_test_bus_timetable,
) -> None:
    query = """
        query {
            bus (weekdays: "weekdays") {
                id, name, districtCode, region, mobileNumber, latitude, longitude,
                routes {
                    sequence,
                    minuteFromStart,
                    info {
                        id, name,
                        company { id, name, telephone }, type { code, name },
                        start {
                            id, name, districtCode, region,
                            mobileNumber, latitude, longitude
                        },
                        end {
                            id, name, districtCode, region,
                            mobileNumber, latitude, longitude
                        },
                        runningTime { up { first, last }, down { first, last } }
                    }
                timetable { weekdays, time },
                realtime { sequence, stop, time, seat, lowFloor, updatedAt },
                log { departureDate, departureTime, vehicleId }
            }
        }
    }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["bus"], list)
    for stop in response.data["bus"]:
        validate_response(stop)
        routes = stop["routes"]
        for route in routes:
            timetable = route["timetable"]
            for item in timetable:
                assert item["weekdays"] == "weekdays"
