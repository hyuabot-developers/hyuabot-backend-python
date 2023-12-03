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


async def list_route() -> list[dict[str, str]]:
    select_query = select(CommuteShuttleRoute)
    return await fetch_all(select_query)


async def get_route(route_name: str) -> dict[str, str] | None:
    select_query = select(CommuteShuttleRoute).where(
        CommuteShuttleRoute.name == route_name,
    )
    return await fetch_one(select_query)


async def create_route(
    new_route: CreateCommuteShuttleRouteRequest,
) -> dict[str, str] | None:
    insert_query = (
        insert(CommuteShuttleRoute)
        .values(
            {
                "route_name": new_route.name,
                "route_description_korean": new_route.route_description_korean,
                "route_description_english": new_route.route_description_english,
            },
        )
        .returning(CommuteShuttleRoute)
    )
    return await fetch_one(insert_query)


async def update_route(
    route_name: str,
    new_route: UpdateCommuteShuttleRouteRequest,
) -> dict[str, str] | None:
    update_query = (
        update(CommuteShuttleRoute)
        .where(CommuteShuttleRoute.name == route_name)
        .values(
            {
                "route_description_korean": new_route.route_description_korean,
                "route_description_english": new_route.route_description_english,
            },
        )
        .returning(CommuteShuttleRoute)
    )
    return await fetch_one(update_query)


async def delete_route(route_name: str) -> None:
    delete_query = delete(CommuteShuttleRoute).where(
        CommuteShuttleRoute.name == route_name,
    )
    await execute_query(delete_query)


async def list_stop() -> list[dict[str, str]]:
    select_query = select(CommuteShuttleStop)
    return await fetch_all(select_query)


async def get_stop(stop_name: str) -> dict[str, str] | None:
    select_query = select(CommuteShuttleStop).where(
        CommuteShuttleStop.name == stop_name,
    )
    return await fetch_one(select_query)


async def create_stop(
    new_stop: CreateCommuteShuttleStopRequest,
) -> dict[str, str] | None:
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
        .returning(CommuteShuttleStop)
    )
    return await fetch_one(insert_query)


async def update_stop(
    stop_name: str,
    new_stop: UpdateCommuteShuttleStopRequest,
) -> dict[str, str] | None:
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
        .returning(CommuteShuttleStop)
    )
    return await fetch_one(update_query)


async def delete_stop(stop_name: str) -> None:
    delete_query = delete(CommuteShuttleStop).where(
        CommuteShuttleStop.name == stop_name,
    )
    await execute_query(delete_query)


async def list_timetable() -> list[dict[str, str]]:
    select_query = select(CommuteShuttleTimetable)
    return await fetch_all(select_query)


async def list_timetable_filter(route_name: str) -> list[dict[str, str]]:
    select_query = select(CommuteShuttleTimetable).where(
        CommuteShuttleTimetable.route_name == route_name,
    )
    return await fetch_all(select_query)


async def get_timetable(
    route_name: str,
    stop_name: str,
) -> dict[str, str] | None:
    select_query = select(CommuteShuttleTimetable).where(
        CommuteShuttleTimetable.route_name == route_name,
        CommuteShuttleTimetable.stop_name == stop_name,
    )
    return await fetch_one(select_query)


async def get_timetable_filter(
    route_name: str,
    sequence: int,
) -> dict[str, str] | None:
    select_query = select(CommuteShuttleTimetable).where(
        CommuteShuttleTimetable.route_name == route_name,
        CommuteShuttleTimetable.sequence == sequence,
    )
    return await fetch_one(select_query)


async def create_timetable(
    new_timetable: CreateCommuteShuttleTimetableRequest,
) -> dict[str, str] | None:
    insert_query = (
        insert(CommuteShuttleTimetable)
        .values(
            {
                "route_name": new_timetable.route_name,
                "stop_name": new_timetable.stop_name,
                "stop_order": new_timetable.sequence,
                "departure_time": new_timetable.departure_time,
            },
        )
        .returning(CommuteShuttleTimetable)
    )
    return await fetch_one(insert_query)


async def update_timetable(
    route_name: str,
    stop_name: str,
    new_timetable: UpdateCommuteShuttleTimetableRequest,
) -> dict[str, str] | None:
    update_query = (
        update(CommuteShuttleTimetable)
        .where(
            CommuteShuttleTimetable.route_name == route_name,
            CommuteShuttleTimetable.stop_name == stop_name,
        )
        .values(
            {
                "stop_order": new_timetable.sequence,
                "departure_time": new_timetable.departure_time,
            },
        )
        .returning(CommuteShuttleTimetable)
    )
    return await fetch_one(update_query)


async def delete_timetable(
    route_name: str,
    stop_name: str,
) -> None:
    delete_query = delete(CommuteShuttleTimetable).where(
        CommuteShuttleTimetable.route_name == route_name,
        CommuteShuttleTimetable.stop_name == stop_name,
    )
    await execute_query(delete_query)
