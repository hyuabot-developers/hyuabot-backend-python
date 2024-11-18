from datetime import time

from sqlalchemy import select, insert, update, delete

from commute_shuttle.schemas import (
    CreateCommuteShuttleRouteRequest,
    UpdateCommuteShuttleRouteRequest,
    CreateCommuteShuttleStopRequest,
    UpdateCommuteShuttleStopRequest,
    CreateCommuteShuttleTimetableRequest,
    UpdateCommuteShuttleTimetableRequest,
)
from database import fetch_all, fetch_one, execute_query
from model.commute_shuttle import (
    CommuteShuttleRoute,
    CommuteShuttleStop,
    CommuteShuttleTimetable,
)
from utils import KST


async def list_route() -> list[CommuteShuttleRoute]:
    select_query = select(CommuteShuttleRoute)
    return await fetch_all(select_query)


async def get_route(route_name: str) -> CommuteShuttleRoute | None:
    select_query = select(CommuteShuttleRoute).where(
        CommuteShuttleRoute.name == route_name,
    )
    return await fetch_one(select_query)


async def create_route(
    new_route: CreateCommuteShuttleRouteRequest,
) -> CommuteShuttleRoute | None:
    insert_query = (
        insert(CommuteShuttleRoute)
        .values(
            {
                "route_name": new_route.name,
                "route_description_korean": new_route.route_description_korean,
                "route_description_english": new_route.route_description_english,
            },
        )
    )
    await execute_query(insert_query)


async def update_route(
    route_name: str,
    new_route: UpdateCommuteShuttleRouteRequest,
) -> CommuteShuttleRoute | None:
    update_query = (
        update(CommuteShuttleRoute)
        .where(CommuteShuttleRoute.name == route_name)
        .values(
            {
                "korean": new_route.route_description_korean,
                "english": new_route.route_description_english,
            },
        )
    )
    await execute_query(update_query)


async def delete_route(route_name: str) -> None:
    delete_query = delete(CommuteShuttleRoute).where(
        CommuteShuttleRoute.name == route_name,
    )
    await execute_query(delete_query)


async def list_stop() -> list[CommuteShuttleStop]:
    select_query = select(CommuteShuttleStop)
    return await fetch_all(select_query)


async def get_stop(stop_name: str) -> CommuteShuttleStop | None:
    select_query = select(CommuteShuttleStop).where(
        CommuteShuttleStop.name == stop_name,
    )
    return await fetch_one(select_query)


async def create_stop(
    new_stop: CreateCommuteShuttleStopRequest,
) -> CommuteShuttleStop | None:
    insert_query = (
        insert(CommuteShuttleStop)
        .values(
            {
                "stop_name": new_stop.name,
                "description": new_stop.description,
                "latitude": new_stop.latitude,
                "longitude": new_stop.longitude,
            },
        )
    )
    await execute_query(insert_query)


async def update_stop(
    stop_name: str,
    new_stop: UpdateCommuteShuttleStopRequest,
) -> CommuteShuttleStop | None:
    update_query = (
        update(CommuteShuttleStop)
        .where(CommuteShuttleStop.name == stop_name)
        .values(
            {
                "description": new_stop.description,
                "latitude": new_stop.latitude,
                "longitude": new_stop.longitude,
            },
        )
    )
    await execute_query(update_query)


async def delete_stop(stop_name: str) -> None:
    delete_query = delete(CommuteShuttleStop).where(
        CommuteShuttleStop.name == stop_name,
    )
    await execute_query(delete_query)


async def list_timetable() -> list[CommuteShuttleTimetable]:
    select_query = select(CommuteShuttleTimetable)
    return await fetch_all(select_query)


async def list_timetable_filter(route_name: str) -> list[CommuteShuttleTimetable]:
    select_query = select(CommuteShuttleTimetable).where(
        CommuteShuttleTimetable.route_name == route_name,
    )
    return await fetch_all(select_query)


async def get_timetable(
    route_name: str,
    stop_name: str,
) -> CommuteShuttleTimetable | None:
    select_query = select(CommuteShuttleTimetable).where(
        CommuteShuttleTimetable.route_name == route_name,
        CommuteShuttleTimetable.stop_name == stop_name,
    )
    return await fetch_one(select_query)


async def get_timetable_filter(
    route_name: str,
    sequence: int,
) -> CommuteShuttleTimetable | None:
    select_query = select(CommuteShuttleTimetable).where(
        CommuteShuttleTimetable.route_name == route_name,
        CommuteShuttleTimetable.sequence == sequence,
    )
    return await fetch_one(select_query)


async def create_timetable(
    new_timetable: CreateCommuteShuttleTimetableRequest,
) -> CommuteShuttleTimetable | None:
    insert_query = (
        insert(CommuteShuttleTimetable)
        .values(
            {
                "route_name": new_timetable.route_name,
                "stop_name": new_timetable.stop_name,
                "stop_order": new_timetable.sequence,
                "departure_time": new_timetable.departure_time.replace(tzinfo=KST),
            },
        )
    )
    await execute_query(insert_query)


async def update_timetable(
    route_name: str,
    stop_name: str,
    new_timetable: UpdateCommuteShuttleTimetableRequest,
) -> CommuteShuttleTimetable | None:
    payload: dict[str, int | time] = {}
    if new_timetable.sequence is not None:
        payload["sequence"] = new_timetable.sequence
    if new_timetable.departure_time is not None:
        payload["time"] = new_timetable.departure_time.replace(tzinfo=KST)
    update_query = (
        update(CommuteShuttleTimetable)
        .where(
            CommuteShuttleTimetable.route_name == route_name,
            CommuteShuttleTimetable.stop_name == stop_name,
        )
        .values(payload)
    )
    await execute_query(update_query)


async def delete_timetable(
    route_name: str,
    stop_name: str,
) -> None:
    delete_query = delete(CommuteShuttleTimetable).where(
        CommuteShuttleTimetable.route_name == route_name,
        CommuteShuttleTimetable.stop_name == stop_name,
    )
    await execute_query(delete_query)
