import pytest
from async_asgi_testclient import TestClient

from query.router import graphql_schema


def validate_response(response: dict) -> None:
    assert isinstance(response["id"], str)
    assert isinstance(response["name"], str)
    assert isinstance(response["sequence"], int)
    assert isinstance(response["routeID"], str)
    assert isinstance(response["timetable"], dict)
    assert isinstance(response["realtime"], dict)
    # Timetable
    timetable = response["timetable"]
    assert isinstance(timetable["up"], list)
    assert isinstance(timetable["down"], list)
    up_timetable = timetable["up"]
    down_timetable = timetable["down"]
    for item in up_timetable:
        assert isinstance(item["weekdays"], bool)
        assert isinstance(item["time"], str)
        assert isinstance(item["start"], dict)
        assert isinstance(item["terminal"], dict)
        start_station = item["start"]
        terminal_station = item["terminal"]
        assert isinstance(start_station["id"], str)
        assert isinstance(start_station["name"], str)
        assert isinstance(terminal_station["id"], str)
        assert isinstance(terminal_station["name"], str)
    for item in down_timetable:
        assert isinstance(item["weekdays"], bool)
        assert isinstance(item["time"], str)
        assert isinstance(item["start"], dict)
        assert isinstance(item["terminal"], dict)
        start_station = item["start"]
        terminal_station = item["terminal"]
        assert isinstance(start_station["id"], str)
        assert isinstance(start_station["name"], str)
        assert isinstance(terminal_station["id"], str)
        assert isinstance(terminal_station["name"], str)
    # Realtime
    realtime = response["realtime"]
    assert isinstance(realtime["up"], list)
    assert isinstance(realtime["down"], list)
    up_realtime = realtime["up"]
    down_realtime = realtime["down"]
    for item in up_realtime:
        assert isinstance(item["sequence"], int)
        assert isinstance(item["location"], str)
        assert isinstance(item["stop"], int)
        assert isinstance(item["time"], float)
        assert isinstance(item["trainNo"], str)
        assert isinstance(item["express"], bool)
        assert isinstance(item["last"], bool)
        assert isinstance(item["status"], int)
        assert isinstance(item["terminal"], dict)
        assert isinstance(item["updatedAt"], str)
        terminal_station = item["terminal"]
        assert isinstance(terminal_station["id"], str)
        assert isinstance(terminal_station["name"], str)
    for item in down_realtime:
        assert isinstance(item["sequence"], int)
        assert isinstance(item["location"], str)
        assert isinstance(item["stop"], int)
        assert isinstance(item["time"], float)
        assert isinstance(item["trainNo"], str)
        assert isinstance(item["express"], bool)
        assert isinstance(item["last"], bool)
        assert isinstance(item["status"], int)
        assert isinstance(item["terminal"], dict)
        assert isinstance(item["updatedAt"], str)
        terminal_station = item["terminal"]
        assert isinstance(terminal_station["id"], str)
        assert isinstance(terminal_station["name"], str)


@pytest.mark.asyncio
async def test_get_subway_query(
    client: TestClient,
    clean_db,
    create_test_subway_realtime,
    create_test_subway_timetable,
) -> None:
    query = """
        query {
            subway {
                id, name, sequence, routeID,
                timetable {
                    up { weekdays, time, start { id, name }, terminal { id, name } },
                    down { weekdays, time, start { id, name }, terminal { id, name } }
                },
                realtime {
                    up {
                        sequence, location, stop, time, trainNo, express, last,
                        status, terminal { id, name }, updatedAt
                    },
                    down {
                        sequence, location, stop, time, trainNo, express, last,
                        status, terminal { id, name }, updatedAt
                    }
                }
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["subway"], list)
    for station in response.data["subway"]:
        validate_response(station)


@pytest.mark.asyncio
async def test_get_subway_query_filter_station_id(
    client: TestClient,
    clean_db,
    create_test_subway_realtime,
    create_test_subway_timetable,
) -> None:
    query = """
        query {
            subway (id_: ["K001"]) {
                id, name, sequence, routeID,
                timetable {
                    up { weekdays, time, start { id, name }, terminal { id, name } },
                    down { weekdays, time, start { id, name }, terminal { id, name } }
                },
                realtime {
                    up {
                        sequence, location, stop, time, trainNo, express, last,
                        status, terminal { id, name }, updatedAt
                    },
                    down {
                        sequence, location, stop, time, trainNo, express, last,
                        status, terminal { id, name }, updatedAt
                    }
                }
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["subway"], list)
    for station in response.data["subway"]:
        assert station["id"] == "K001"
        validate_response(station)


@pytest.mark.asyncio
async def test_get_subway_query_filter_station_name(
    client: TestClient,
    clean_db,
    create_test_subway_realtime,
    create_test_subway_timetable,
) -> None:
    query = """
        query {
            subway (name: "test_station_name") {
                id, name, sequence, routeID,
                timetable {
                    up { weekdays, time, start { id, name }, terminal { id, name } },
                    down { weekdays, time, start { id, name }, terminal { id, name } }
                },
                realtime {
                    up {
                        sequence, location, stop, time, trainNo, express, last,
                        status, terminal { id, name }, updatedAt
                    },
                    down {
                        sequence, location, stop, time, trainNo, express, last,
                        status, terminal { id, name }, updatedAt
                    }
                }
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["subway"], list)
    for station in response.data["subway"]:
        assert "test_station_name" in station["name"]
        validate_response(station)


@pytest.mark.asyncio
async def test_get_subway_query_filter_start_time(
    client: TestClient,
    clean_db,
    create_test_subway_realtime,
    create_test_subway_timetable,
) -> None:
    query = """
        query {
            subway (start: "00:05:00") {
                id, name, sequence, routeID,
                timetable {
                    up { weekdays, time, start { id, name }, terminal { id, name } },
                    down { weekdays, time, start { id, name }, terminal { id, name } }
                },
                realtime {
                    up {
                        sequence, location, stop, time, trainNo, express, last,
                        status, terminal { id, name }, updatedAt
                    },
                    down {
                        sequence, location, stop, time, trainNo, express, last,
                        status, terminal { id, name }, updatedAt
                    }
                }
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["subway"], list)
    for station in response.data["subway"]:
        validate_response(station)
        timetable = station["timetable"]
        up_timetable = timetable["up"]
        down_timetable = timetable["down"]
        for item in up_timetable:
            assert item["time"] >= "00:05:00"
        for item in down_timetable:
            assert item["time"] >= "00:05:00"


@pytest.mark.asyncio
async def test_get_subway_query_filter_end_time(
    client: TestClient,
    clean_db,
    create_test_subway_realtime,
    create_test_subway_timetable,
) -> None:
    query = """
        query {
            subway (end: "00:05:00") {
                id, name, sequence, routeID,
                timetable {
                    up { weekdays, time, start { id, name }, terminal { id, name } },
                    down { weekdays, time, start { id, name }, terminal { id, name } }
                },
                realtime {
                    up {
                        sequence, location, stop, time, trainNo, express, last,
                        status, terminal { id, name }, updatedAt
                    },
                    down {
                        sequence, location, stop, time, trainNo, express, last,
                        status, terminal { id, name }, updatedAt
                    }
                }
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["subway"], list)
    for station in response.data["subway"]:
        validate_response(station)
        timetable = station["timetable"]
        up_timetable = timetable["up"]
        down_timetable = timetable["down"]
        for item in up_timetable:
            assert item["time"] <= "00:05:00"
        for item in down_timetable:
            assert item["time"] <= "00:05:00"


@pytest.mark.asyncio
async def test_get_subway_query_filter_weekdays(
    client: TestClient,
    clean_db,
    create_test_subway_realtime,
    create_test_subway_timetable,
) -> None:
    query = """
        query {
            subway (weekdays: true) {
                id, name, sequence, routeID,
                timetable {
                    up { weekdays, time, start { id, name }, terminal { id, name } },
                    down { weekdays, time, start { id, name }, terminal { id, name } }
                },
                realtime {
                    up {
                        sequence, location, stop, time, trainNo, express, last,
                        status, terminal { id, name }, updatedAt
                    },
                    down {
                        sequence, location, stop, time, trainNo, express, last,
                        status, terminal { id, name }, updatedAt
                    }
                }
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["subway"], list)
    for station in response.data["subway"]:
        validate_response(station)
        timetable = station["timetable"]
        up_timetable = timetable["up"]
        down_timetable = timetable["down"]
        for item in up_timetable:
            assert item["weekdays"] is True
        for item in down_timetable:
            assert item["weekdays"] is True


@pytest.mark.asyncio
async def test_get_subway_query_filter_weekends(
    client: TestClient,
    clean_db,
    create_test_subway_realtime,
    create_test_subway_timetable,
) -> None:
    query = """
        query {
            subway (weekdays: false) {
                id, name, sequence, routeID,
                timetable {
                    up { weekdays, time, start { id, name }, terminal { id, name } },
                    down { weekdays, time, start { id, name }, terminal { id, name } }
                },
                realtime {
                    up {
                        sequence, location, stop, time, trainNo, express, last,
                        status, terminal { id, name }, updatedAt
                    },
                    down {
                        sequence, location, stop, time, trainNo, express, last,
                        status, terminal { id, name }, updatedAt
                    }
                }
            }
        }
    """
    response = await graphql_schema.execute(query)
    assert response.errors is None
    assert response.data is not None
    assert isinstance(response.data["subway"], list)
    for station in response.data["subway"]:
        validate_response(station)
        timetable = station["timetable"]
        up_timetable = timetable["up"]
        down_timetable = timetable["down"]
        for item in up_timetable:
            assert item["weekdays"] is False
        for item in down_timetable:
            assert item["weekdays"] is False
