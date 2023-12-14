import datetime
from typing import Any

from sqlalchemy import insert, select, delete, update

from database import fetch_one, fetch_all, execute_query
from model.subway import (
    SubwayStation,
    SubwayRoute,
    SubwayRouteStation,
    SubwayTimetable,
    SubwayRealtime,
)
from subway.dependancies import create_valid_timetable
from subway.schemas import (
    CreateSubwayStation,
    CreateSubwayRoute,
    CreateSubwayRouteStation,
    UpdateSubwayRoute,
    UpdateSubwayRouteStation,
    CreateSubwayTimetable,
)
from utils import KST


async def create_station_name(
    new_station_name: CreateSubwayStation,
) -> dict[str, str] | None:
    insert_query = (
        insert(SubwayStation)
        .values(
            {
                "station_name": new_station_name.name,
            },
        )
        .returning(SubwayStation)
    )

    return await fetch_one(insert_query)


async def get_station_name(station_name: str) -> dict[str, str] | None:
    select_query = select(SubwayStation).where(SubwayStation.name == station_name)
    return await fetch_one(select_query)


async def list_station_name() -> list[dict[str, str]]:
    select_query = select(SubwayStation)
    return await fetch_all(select_query)


async def list_station_name_filter(station_name: str) -> list[dict[str, str]]:
    select_query = select(SubwayStation).filter(
        SubwayStation.name.like(f"%{station_name}%"),
    )
    return await fetch_all(select_query)


async def delete_station_name(station_name: str) -> None:
    delete_query = delete(SubwayStation).where(SubwayStation.name == station_name)
    await execute_query(delete_query)


async def create_route(
    new_route: CreateSubwayRoute,
) -> dict[str, str] | None:
    insert_query = (
        insert(SubwayRoute)
        .values(
            {
                "route_id": new_route.id,
                "route_name": new_route.name,
            },
        )
        .returning(SubwayRoute)
    )

    return await fetch_one(insert_query)


async def get_route(route_id: int) -> dict[str, str] | None:
    select_query = select(SubwayRoute).where(SubwayRoute.id == route_id)
    return await fetch_one(select_query)


async def list_route() -> list[dict[str, str]]:
    select_query = select(SubwayRoute)
    return await fetch_all(select_query)


async def list_route_filter(route_name: str) -> list[dict[str, str]]:
    select_query = select(SubwayRoute).filter(SubwayRoute.name.like(f"%{route_name}%"))
    return await fetch_all(select_query)


async def update_route(
    route_id: int,
    payload: UpdateSubwayRoute,
) -> None:
    update_query = (
        update(SubwayRoute)
        .where(
            SubwayRoute.id == route_id,
        )
        .values(
            {
                "route_name": payload.name,
            },
        )
        .returning(SubwayRoute)
    )

    return await execute_query(update_query)


async def delete_route(route_id: int) -> None:
    delete_query = delete(SubwayRoute).where(SubwayRoute.id == route_id)
    await execute_query(delete_query)


async def create_route_station(
    new_station: CreateSubwayRouteStation,
) -> dict[str, Any] | None:
    insert_query = (
        insert(SubwayRouteStation)
        .values(
            {
                "station_id": new_station.id,
                "station_name": new_station.name,
                "route_id": new_station.route_id,
                "station_sequence": new_station.sequence,
                "cumulative_time": new_station.cumulative_time,
            },
        )
        .returning(SubwayRouteStation)
    )

    return await fetch_one(insert_query)


async def get_route_station(station_id: str) -> dict[str, Any] | None:
    select_query = select(SubwayRouteStation).where(SubwayRouteStation.id == station_id)
    return await fetch_one(select_query)


async def list_route_station() -> list[dict[str, Any]]:
    select_query = select(SubwayRouteStation)
    return await fetch_all(select_query)


async def list_route_station_filter(route_id: int) -> list[dict[str, str]]:
    select_query = select(SubwayRouteStation).filter(
        SubwayRouteStation.route_id == route_id,
    )
    return await fetch_all(select_query)


async def update_route_station(
    station_id: str,
    payload: UpdateSubwayRouteStation,
) -> dict[str, str] | None:
    new_data: dict[str, str | int | datetime.timedelta] = {}
    if payload.name:
        new_data["station_name"] = payload.name
    if payload.sequence:
        new_data["station_sequence"] = payload.sequence
    if payload.cumulative_time:
        new_data["cumulative_time"] = payload.cumulative_time
    update_query = (
        update(SubwayRouteStation)
        .where(
            SubwayRouteStation.id == station_id,
        )
        .values(new_data)
        .returning(SubwayRouteStation)
    )

    await execute_query(update_query)

    select_query = select(SubwayRouteStation).where(SubwayRouteStation.id == station_id)
    return await fetch_one(select_query)


async def delete_route_station(station_id: str) -> None:
    delete_query = delete(SubwayRouteStation).where(SubwayRouteStation.id == station_id)
    await execute_query(delete_query)


async def get_timetable_by_station(station_id: str) -> list[dict[str, Any]]:
    select_query = select(SubwayTimetable).where(
        SubwayTimetable.station_id == station_id,
    )
    return await fetch_all(select_query)


async def get_timetable(
    station_id: str,
    weekday: str,
    heading: str,
    departure_time: datetime.time,
) -> dict[str, Any] | None:
    select_query = select(SubwayTimetable).where(
        SubwayTimetable.station_id == station_id,
        SubwayTimetable.is_weekdays == weekday,
        SubwayTimetable.heading == heading,
        SubwayTimetable.departure_time == departure_time,
    )
    return await fetch_one(select_query)


async def create_timetable(
    station_id: str,
    new_timetable: CreateSubwayTimetable,
) -> dict[str, Any] | None:
    await create_valid_timetable(station_id, new_timetable)
    insert_query = (
        insert(SubwayTimetable)
        .values(
            {
                "station_id": station_id,
                "start_station_id": new_timetable.start_station_id,
                "terminal_station_id": new_timetable.terminal_station_id,
                "departure_time": new_timetable.departure_time.replace(tzinfo=KST),
                "weekday": new_timetable.weekday,
                "heading": new_timetable.heading,
            },
        )
        .returning(SubwayTimetable)
    )

    return await fetch_one(insert_query)


async def delete_timetable(
    station_id: str,
    weekday: str,
    heading: str,
    departure_time: datetime.time,
) -> None:
    delete_query = delete(SubwayTimetable).where(
        SubwayTimetable.station_id == station_id,
        SubwayTimetable.is_weekdays == weekday,
        SubwayTimetable.heading == heading,
        SubwayTimetable.departure_time == departure_time,
    )
    await execute_query(delete_query)


async def get_realtime(station_id: str) -> list[dict[str, Any]]:
    select_query = select(SubwayRealtime).where(
        SubwayRealtime.station_id == station_id,
    )
    return await fetch_all(select_query)
