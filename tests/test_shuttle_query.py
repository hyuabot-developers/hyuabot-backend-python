from datetime import datetime

import pytest
from async_asgi_testclient import TestClient
from pytz import timezone

from query.router import graphql_schema


def validate_stop_response(stop: dict):
    assert "name" in stop
    assert "latitude" in stop
    assert "longitude" in stop
    assert "routes" in stop
    for route in stop["routes"]:
        assert "name" in route
        assert "tag" in route
        assert "start" in route
        assert "end" in route
        assert "korean" in route
        assert "english" in route


@pytest.mark.asyncio
async def test_get_shuttle_stop_query(
    client: TestClient,
    clean_db,
    create_test_shuttle_period,
    create_test_shuttle_timetable,
) -> None:
    query = """
        query {
            shuttle {
                stop {name, latitude, longitude, routes {
                    name, tag, start, end, korean, english
                }}
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["shuttle"], dict)
    stops = response.data["shuttle"]["stop"]
    assert isinstance(stops, list)
    for stop in stops:
        validate_stop_response(stop)


@pytest.mark.asyncio
async def test_get_shuttle_stop_query_name_filter(
    client: TestClient,
    clean_db,
    create_test_shuttle_period,
    create_test_shuttle_timetable,
) -> None:
    query = """
        query {
            shuttle (stopName: ["test_stop1"]) {
                stop {name, latitude, longitude, routes {
                    name, tag, start, end, korean, english
                }}
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["shuttle"], dict)
    stops = response.data["shuttle"]["stop"]
    assert isinstance(stops, list)
    for stop in stops:
        assert "test_stop1" in stop["name"]
        validate_stop_response(stop)


@pytest.mark.asyncio
async def test_get_shuttle_period(
    client: TestClient,
    clean_db,
    create_test_shuttle_period,
) -> None:
    query = """
        query {
            shuttle {
                period {type, start, end}
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["shuttle"], dict)
    periods = response.data["shuttle"]["period"]
    assert isinstance(periods, list)
    for period in periods:
        assert "type" in period
        assert "start" in period
        assert "end" in period


@pytest.mark.asyncio
async def test_get_shuttle_period_start_filter(
    client: TestClient,
    clean_db,
    create_test_shuttle_period,
) -> None:
    query = """
        query {
            shuttle (periodStart: "2021-01-01") {
                period {type, start, end}
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["shuttle"], dict)
    periods = response.data["shuttle"]["period"]
    assert isinstance(periods, list)
    for period in periods:
        assert period["start"] <= "2021-01-01T00:00:00+09:00"


@pytest.mark.asyncio
async def test_get_shuttle_period_end_filter(
    client: TestClient,
    clean_db,
    create_test_shuttle_period,
) -> None:
    query = """
        query {
            shuttle (periodEnd: "2021-01-01") {
                period {type, start, end}
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["shuttle"], dict)
    periods = response.data["shuttle"]["period"]
    assert isinstance(periods, list)
    for period in periods:
        assert period["end"] >= "2021-01-01T00:00:00+09:00"


@pytest.mark.asyncio
async def test_get_shuttle_period_current_filter(
    client: TestClient,
    clean_db,
    create_test_shuttle_period,
) -> None:
    query = """
        query {
            shuttle (periodCurrent: true) {
                period {type, start, end}
            }
        }
    """
    now = (
        datetime.now()
        .astimezone(tz=timezone("Asia/Seoul"))
        .strftime("%Y-%m-%dT%H:%M:%S%z")
    )
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["shuttle"], dict)
    periods = response.data["shuttle"]["period"]
    assert isinstance(periods, list)
    for period in periods:
        assert period["start"] <= now
        assert period["end"] >= now


@pytest.mark.asyncio
async def test_get_shuttle_holiday(
    client: TestClient,
    clean_db,
    create_test_shuttle_period,
    create_test_shuttle_holiday,
) -> None:
    query = """
        query {
            shuttle {
                holiday {date, type, calendar}
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["shuttle"], dict)
    holidays = response.data["shuttle"]["holiday"]
    assert isinstance(holidays, list)
    for holiday in holidays:
        assert "date" in holiday
        assert "type" in holiday
        assert "calendar" in holiday


@pytest.mark.asyncio
async def test_get_shuttle_route(
    client: TestClient,
    clean_db,
    create_test_shuttle_period,
    create_test_shuttle_route,
    create_test_shuttle_route_stop,
) -> None:
    query = """
        query {
            shuttle {
                route {
                    name, tag, start, end, korean, english, end, stops {
                        name, sequence
                    }
                }
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["shuttle"], dict)
    routes = response.data["shuttle"]["route"]
    assert isinstance(routes, list)
    for route in routes:
        assert "name" in route
        assert "start" in route
        assert "end" in route
        assert "korean" in route
        assert "english" in route
        assert "tag" in route
        stops = route["stops"]
        assert isinstance(stops, list)
        for stop in stops:
            assert "name" in stop
            assert "sequence" in stop


@pytest.mark.asyncio
async def test_get_shuttle_route_name_filter(
    client: TestClient,
    clean_db,
    create_test_shuttle_period,
    create_test_shuttle_route,
    create_test_shuttle_route_stop,
) -> None:
    query = """
        query {
            shuttle (routeName: ["test_route1"]) {
                route {
                    name, tag, start, end, korean, english, end, stops {
                        name, sequence
                    }
                }
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["shuttle"], dict)
    routes = response.data["shuttle"]["route"]
    assert isinstance(routes, list)
    for route in routes:
        assert "test_route1" in route["name"]
        assert "start" in route
        assert "end" in route
        assert "korean" in route
        assert "english" in route
        assert "tag" in route
        stops = route["stops"]
        assert isinstance(stops, list)
        for stop in stops:
            assert "name" in stop
            assert "sequence" in stop


@pytest.mark.asyncio
async def test_get_shuttle_route_tag_filter(
    client: TestClient,
    clean_db,
    create_test_shuttle_period,
    create_test_shuttle_route,
    create_test_shuttle_route_stop,
) -> None:
    query = """
        query {
            shuttle (routeTag: ["test_tag"]) {
                route {
                    name, tag, start, end, korean, english, end, stops {
                        name, sequence
                    }
                }
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["shuttle"], dict)
    routes = response.data["shuttle"]["route"]
    assert isinstance(routes, list)
    for route in routes:
        assert "test_tag" in route["tag"]
        assert "start" in route
        assert "end" in route
        assert "korean" in route
        assert "english" in route
        assert "name" in route
        stops = route["stops"]
        assert isinstance(stops, list)
        for stop in stops:
            assert "name" in stop
            assert "sequence" in stop


@pytest.mark.asyncio
async def test_get_shuttle_route_start_stop_filter(
    client: TestClient,
    clean_db,
    create_test_shuttle_period,
    create_test_shuttle_route,
    create_test_shuttle_route_stop,
) -> None:
    query = """
        query {
            shuttle (routeStart: ["test_stop1"]) {
                route {
                    name, tag, start, end, korean, english, end, stops {
                        name, sequence
                    }
                }
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["shuttle"], dict)
    routes = response.data["shuttle"]["route"]
    assert isinstance(routes, list)
    for route in routes:
        assert "test_stop1" in route["start"]
        assert "end" in route
        assert "korean" in route
        assert "english" in route
        assert "name" in route
        assert "tag" in route
        stops = route["stops"]
        assert isinstance(stops, list)
        for stop in stops:
            assert "name" in stop
            assert "sequence" in stop


@pytest.mark.asyncio
async def test_get_shuttle_route_end_stop_filter(
    client: TestClient,
    clean_db,
    create_test_shuttle_period,
    create_test_shuttle_route,
    create_test_shuttle_route_stop,
) -> None:
    query = """
        query {
            shuttle (routeEnd: ["test_stop2"]) {
                route {
                    name, tag, start, end, korean, english, end, stops {
                        name, sequence
                    }
                }
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["shuttle"], dict)
    routes = response.data["shuttle"]["route"]
    assert isinstance(routes, list)
    for route in routes:
        assert "test_stop2" in route["end"]
        assert "start" in route
        assert "korean" in route
        assert "english" in route
        assert "name" in route
        assert "tag" in route
        stops = route["stops"]
        assert isinstance(stops, list)
        for stop in stops:
            assert "name" in stop
            assert "sequence" in stop


@pytest.mark.asyncio
async def test_get_shuttle_timetable(
    client: TestClient,
    clean_db,
    create_test_shuttle_period,
    create_test_shuttle_route_stop,
    create_test_shuttle_timetable,
) -> None:
    query = """
        query {
            shuttle {
                timetable {
                    id, period, weekdays, route, tag, stop, time, via {
                        stop, time
                    }
                }
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["shuttle"], dict)
    timetable = response.data["shuttle"]["timetable"]
    assert isinstance(timetable, list)
    for item in timetable:
        assert "id" in item
        assert "period" in item
        assert "weekdays" in item
        assert "route" in item
        assert "tag" in item
        assert "stop" in item
        assert "time" in item
        assert "via" in item


@pytest.mark.asyncio
async def test_get_shuttle_timetable_weekdays_filter(
    client: TestClient,
    clean_db,
    create_test_shuttle_period,
    create_test_shuttle_route_stop,
    create_test_shuttle_timetable,
) -> None:
    query = """
        query {
            shuttle (weekdays: [true]) {
                timetable {
                    id, period, weekdays, route, tag, stop, time, via {
                        stop, time
                    }
                }
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["shuttle"], dict)
    timetable = response.data["shuttle"]["timetable"]
    assert isinstance(timetable, list)
    for item in timetable:
        assert "id" in item
        assert "period" in item
        assert item["weekdays"] is True
        assert "route" in item
        assert "tag" in item
        assert "stop" in item
        assert "time" in item
        assert "via" in item


@pytest.mark.asyncio
async def test_get_shuttle_timetable_weekends_filter(
    client: TestClient,
    clean_db,
    create_test_shuttle_period,
    create_test_shuttle_route_stop,
    create_test_shuttle_timetable,
) -> None:
    query = """
        query {
            shuttle (weekdays: [false]) {
                timetable {
                    id, period, weekdays, route, tag, stop, time, via {
                        stop, time
                    }
                }
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["shuttle"], dict)
    timetable = response.data["shuttle"]["timetable"]
    assert isinstance(timetable, list)
    for item in timetable:
        assert "id" in item
        assert "period" in item
        assert item["weekdays"] is False
        assert "route" in item
        assert "tag" in item
        assert "stop" in item
        assert "time" in item
        assert "via" in item


@pytest.mark.asyncio
async def test_get_shuttle_timetable_period_filter(
    client: TestClient,
    clean_db,
    create_test_shuttle_period,
    create_test_shuttle_route_stop,
    create_test_shuttle_timetable,
) -> None:
    query = """
        query {
            shuttle (period: ["semester"]) {
                timetable {
                    id, period, weekdays, route, tag, stop, time, via {
                        stop, time
                    }
                }
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["shuttle"], dict)
    timetable = response.data["shuttle"]["timetable"]
    assert isinstance(timetable, list)
    for item in timetable:
        assert "id" in item
        assert item["period"] == "semester"
        assert "weekdays" in item
        assert "route" in item
        assert "tag" in item
        assert "stop" in item
        assert "time" in item
        assert "via" in item


@pytest.mark.asyncio
async def test_get_shuttle_timetable_period_not_found(
    client: TestClient,
    clean_db,
    create_test_shuttle_period,
    create_test_shuttle_route_stop,
    create_test_shuttle_timetable,
) -> None:
    query = """
        query {
            shuttle (timestamp: "2021-01-01T00:00:00+09:00") {
                timetable {
                    id, period, weekdays, route, tag, stop, time, via {
                        stop, time
                    }
                }
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is not None


@pytest.mark.asyncio
async def test_get_shuttle_timetable_holiday_filter(
    client: TestClient,
    clean_db,
    create_test_shuttle_period,
    create_test_shuttle_holiday,
    create_test_shuttle_route_stop,
    create_test_shuttle_timetable,
) -> None:
    query = """
        query {
            shuttle (timestamp: "2024-01-01T00:00:00+09:00") {
                timetable {
                    id, period, weekdays, route, tag, stop, time, via {
                        stop, time
                    }
                }
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["shuttle"], dict)
    timetable = response.data["shuttle"]["timetable"]
    assert isinstance(timetable, list)
    for item in timetable:
        assert "id" in item
        assert "period" in item
        assert item["weekdays"] is False
        assert "route" in item
        assert "tag" in item
        assert "stop" in item
        assert "time" in item
        assert "via" in item


@pytest.mark.asyncio
async def test_get_shuttle_timetable_halt_filter(
    client: TestClient,
    clean_db,
    create_test_shuttle_period,
    create_test_shuttle_holiday,
    create_test_shuttle_route_stop,
    create_test_shuttle_timetable,
) -> None:
    query = """
        query {
            shuttle (timestamp: "2024-01-02T00:00:00+09:00") {
                timetable {
                    id, period, weekdays, route, tag, stop, time, via {
                        stop, time
                    }
                }
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["shuttle"], dict)
    timetable = response.data["shuttle"]["timetable"]
    assert isinstance(timetable, list)
    assert len(timetable) == 0


@pytest.mark.asyncio
async def test_get_shuttle_timetable_start_filter(
    client: TestClient,
    clean_db,
    create_test_shuttle_period,
    create_test_shuttle_holiday,
    create_test_shuttle_route_stop,
    create_test_shuttle_timetable,
) -> None:
    query = """
        query {
            shuttle (start: "05:00:00") {
                timetable {
                    id, period, weekdays, route, tag, stop, time, via {
                        stop, time
                    }
                }
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["shuttle"], dict)
    timetable = response.data["shuttle"]["timetable"]
    assert isinstance(timetable, list)
    for item in timetable:
        assert "id" in item
        assert "period" in item
        assert "weekdays" in item
        assert "route" in item
        assert "tag" in item
        assert "stop" in item
        assert item["time"] >= "05:00:00"
        assert "via" in item


@pytest.mark.asyncio
async def test_get_shuttle_timetable_end_filter(
    client: TestClient,
    clean_db,
    create_test_shuttle_period,
    create_test_shuttle_holiday,
    create_test_shuttle_route_stop,
    create_test_shuttle_timetable,
) -> None:
    query = """
        query {
            shuttle (end: "05:00:00") {
                timetable {
                    id, period, weekdays, route, tag, stop, time, via {
                        stop, time
                    }
                }
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["shuttle"], dict)
    timetable = response.data["shuttle"]["timetable"]
    assert isinstance(timetable, list)
    for item in timetable:
        assert "id" in item
        assert "period" in item
        assert "weekdays" in item
        assert "route" in item
        assert "tag" in item
        assert "stop" in item
        assert item["time"] <= "05:00:00"
        assert "via" in item


@pytest.mark.asyncio
async def test_get_shuttle_grouped_timetable(
    client: TestClient,
    clean_db,
    create_test_shuttle_period,
    create_test_shuttle_route_stop,
    create_test_shuttle_timetable,
) -> None:
    query = """
        query {
            shuttle {
                groupedTimetable {
                    id, period, weekdays, route, tag, stop, time, destination
                }
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["shuttle"], dict)
    timetable = response.data["shuttle"]["groupedTimetable"]
    assert isinstance(timetable, list)
    for item in timetable:
        assert "id" in item
        assert "period" in item
        assert item["weekdays"] is False
        assert "route" in item
        assert "tag" in item
        assert "stop" in item
        assert "time" in item
        assert "destination" in item
