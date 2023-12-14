import datetime
from typing import Any

from sqlalchemy import select, insert, delete, update

from bus.schemas import (
    CreateBusRouteRequest,
    UpdateBusRouteRequest,
    CreateBusStopRequest,
    UpdateBusStopRequest,
    CreateBusRouteStopRequest,
    UpdateBusRouteStopRequest,
    CreateBusTimetableRequest,
)
from database import fetch_all, fetch_one, execute_query
from model.bus import BusRoute, BusStop, BusRouteStop, BusTimetable, BusRealtime
from utils import KST


async def list_routes() -> list[dict[str, Any]]:
    select_query = select(BusRoute)
    return await fetch_all(select_query)


async def list_routes_filter(
    name: str | None = None,
    type_: str | None = None,
    company: str | None = None,
) -> list[dict[str, Any]]:
    conditions = []
    if type_ is not None:
        conditions.append(BusRoute.type_name == type_)
    if name is not None:
        conditions.append(BusRoute.name.like(f"%{name}%"))
    if company is not None:
        conditions.append(BusRoute.company_name.like(f"%{company}%"))
    select_query = select(BusRoute).where(*conditions)
    return await fetch_all(select_query)


async def get_route(route_id: int) -> dict[str, Any] | None:
    select_query = select(BusRoute).where(BusRoute.id == route_id)
    return await fetch_one(select_query)


async def create_route(new_holiday: CreateBusRouteRequest) -> dict[str, Any] | None:
    insert_query = (
        insert(BusRoute)
        .values(
            {
                "route_id": new_holiday.id,
                "route_name": new_holiday.name,
                "route_type_code": new_holiday.type_code,
                "route_type_name": new_holiday.type_name,
                "company_id": new_holiday.company_id,
                "company_name": new_holiday.company_name,
                "company_telephone": new_holiday.company_telephone,
                "district_code": new_holiday.district_code,
                "up_first_time": new_holiday.up_first_time.replace(tzinfo=KST),
                "up_last_time": new_holiday.up_last_time.replace(tzinfo=KST),
                "down_first_time": new_holiday.down_first_time.replace(tzinfo=KST),
                "down_last_time": new_holiday.down_last_time.replace(tzinfo=KST),
                "start_stop_id": new_holiday.start_stop_id,
                "end_stop_id": new_holiday.end_stop_id,
            },
        )
        .returning(BusRoute)
    )
    return await fetch_one(insert_query)


async def update_route(
    route_id: int,
    payload: UpdateBusRouteRequest,
) -> dict[str, Any] | None:
    update_query = (
        update(BusRoute)
        .where(BusRoute.id == route_id)
        .values(
            {
                "route_name": (
                    payload.name if payload.name is not None else BusRoute.name
                ),
                "route_type_code": (
                    payload.type_code
                    if payload.type_code is not None
                    else BusRoute.type_code
                ),
                "route_type_name": (
                    payload.type_name
                    if payload.type_name is not None
                    else BusRoute.type_name
                ),
                "company_id": (
                    payload.company_id
                    if payload.company_id is not None
                    else BusRoute.company_id
                ),
                "company_name": (
                    payload.company_name
                    if payload.company_name is not None
                    else BusRoute.company_name
                ),
                "company_telephone": (
                    payload.company_telephone
                    if payload.company_telephone is not None
                    else BusRoute.company_telephone
                ),
                "district_code": (
                    payload.district_code
                    if payload.district_code is not None
                    else BusRoute.district
                ),
                "up_first_time": (
                    payload.up_first_time.replace(tzinfo=KST)
                    if payload.up_first_time is not None
                    else BusRoute.up_first_time
                ),
                "up_last_time": (
                    payload.up_last_time.replace(tzinfo=KST)
                    if payload.up_last_time is not None
                    else BusRoute.up_last_time
                ),
                "down_first_time": (
                    payload.down_first_time.replace(tzinfo=KST)
                    if payload.down_first_time is not None
                    else BusRoute.down_first_time
                ),
                "down_last_time": (
                    payload.down_last_time.replace(tzinfo=KST)
                    if payload.down_last_time is not None
                    else BusRoute.down_last_time
                ),
                "start_stop_id": (
                    payload.start_stop_id
                    if payload.start_stop_id is not None
                    else BusRoute.start_stop_id
                ),
                "end_stop_id": (
                    payload.end_stop_id
                    if payload.end_stop_id is not None
                    else BusRoute.end_stop_id
                ),
            },
        )
        .returning(BusRoute)
    )
    return await fetch_one(update_query)


async def delete_route(route_id: int) -> None:
    delete_query = delete(BusRoute).where(BusRoute.id == route_id)
    await execute_query(delete_query)


async def list_stops() -> list[dict[str, Any]]:
    select_query = select(BusStop)
    return await fetch_all(select_query)


async def list_stops_filter(name: str) -> list[dict[str, Any]]:
    select_query = select(BusStop).where(BusStop.name.like(f"%{name}%"))
    return await fetch_all(select_query)


async def get_stop(stop_id: int) -> dict[str, Any] | None:
    select_query = select(BusStop).where(BusStop.id == stop_id)
    return await fetch_one(select_query)


async def create_stop(new_stop: CreateBusStopRequest) -> dict[str, Any] | None:
    insert_query = (
        insert(BusStop)
        .values(
            {
                "stop_id": new_stop.id,
                "stop_name": new_stop.name,
                "district_code": new_stop.district_code,
                "mobile_number": new_stop.mobile_number,
                "region_name": new_stop.region_name,
                "latitude": new_stop.latitude,
                "longitude": new_stop.longitude,
            },
        )
        .returning(BusStop)
    )
    return await fetch_one(insert_query)


async def update_stop(
    stop_id: int,
    payload: UpdateBusStopRequest,
) -> dict[str, Any] | None:
    update_query = (
        update(BusStop)
        .where(BusStop.id == stop_id)
        .values(
            {
                "stop_name": (
                    payload.name if payload.name is not None else BusStop.name
                ),
                "district_code": (
                    payload.district_code
                    if payload.district_code is not None
                    else BusStop.district
                ),
                "mobile_number": (
                    payload.mobile_number
                    if payload.mobile_number is not None
                    else BusStop.mobile_no
                ),
                "region_name": (
                    payload.region_name
                    if payload.region_name is not None
                    else BusStop.region
                ),
                "latitude": (
                    payload.latitude
                    if payload.latitude is not None
                    else BusStop.latitude
                ),
                "longitude": (
                    payload.longitude
                    if payload.longitude is not None
                    else BusStop.longitude
                ),
            },
        )
        .returning(BusStop)
    )
    return await fetch_one(update_query)


async def delete_stop(stop_id: int) -> None:
    delete_query = delete(BusStop).where(BusStop.id == stop_id)
    await execute_query(delete_query)


async def list_route_stops(route_id: int) -> list[dict[str, Any]]:
    select_query = select(BusRouteStop).where(BusRouteStop.route_id == route_id)
    return await fetch_all(select_query)


async def get_route_stop(route_id: int, stop_id: int) -> dict[str, Any] | None:
    select_query = select(BusRouteStop).where(
        BusRouteStop.route_id == route_id,
        BusRouteStop.stop_id == stop_id,
    )
    return await fetch_one(select_query)


async def create_route_stop(
    route_id: int,
    new_route_stop: CreateBusRouteStopRequest,
) -> dict[str, Any] | None:
    insert_query = (
        insert(BusRouteStop)
        .values(
            {
                "route_id": route_id,
                "stop_id": new_route_stop.stop_id,
                "stop_sequence": new_route_stop.sequence,
                "start_stop_id": new_route_stop.start_stop_id,
            },
        )
        .returning(BusRouteStop)
    )
    return await fetch_one(insert_query)


async def update_route_stop(
    route_id: int,
    stop_id: int,
    payload: UpdateBusRouteStopRequest,
) -> dict[str, Any] | None:
    update_query = (
        update(BusRouteStop)
        .where(
            BusRouteStop.route_id == route_id,
            BusRouteStop.stop_id == stop_id,
        )
        .values(
            {
                "stop_sequence": (
                    payload.sequence
                    if payload.sequence is not None
                    else BusRouteStop.sequence
                ),
                "start_stop_id": (
                    payload.start_stop_id
                    if payload.start_stop_id is not None
                    else BusRouteStop.start_stop_id
                ),
            },
        )
        .returning(BusRouteStop)
    )
    return await fetch_one(update_query)


async def delete_route_stop(route_id: int, stop_id: int) -> None:
    delete_query = delete(BusRouteStop).where(
        BusRouteStop.route_id == route_id,
        BusRouteStop.stop_id == stop_id,
    )
    await execute_query(delete_query)


async def list_timetable() -> list[dict[str, Any]]:
    select_query = select(BusTimetable)
    return await fetch_all(select_query)


async def list_timetable_filter(
    route_id: int | None = None,
    start_stop_id: int | None = None,
    weekday: str | None = None,
    start: datetime.time | None = None,
    end: datetime.time | None = None,
) -> list[dict[str, Any]]:
    conditions = []
    if route_id is not None:
        conditions.append(BusTimetable.route_id == route_id)
    if start_stop_id is not None:
        conditions.append(BusTimetable.start_stop_id == start_stop_id)
    if weekday is not None:
        conditions.append(BusTimetable.weekday == weekday)
    if start is not None:
        conditions.append(BusTimetable.departure_time >= start)
    if end is not None:
        conditions.append(BusTimetable.departure_time <= end)
    select_query = select(BusTimetable).where(*conditions)
    return await fetch_all(select_query)


async def get_timetable(
    route_id: int,
    start_stop_id: int,
    weekday: str,
    departure_time: datetime.time,
) -> dict[str, Any] | None:
    select_query = select(BusTimetable).where(
        BusTimetable.route_id == route_id,
        BusTimetable.start_stop_id == start_stop_id,
        BusTimetable.weekday == weekday,
        BusTimetable.departure_time == departure_time,
    )
    return await fetch_one(select_query)


async def create_timetable(
    new_timetable: CreateBusTimetableRequest,
) -> dict[str, Any] | None:
    insert_query = (
        insert(BusTimetable)
        .values(
            {
                "route_id": new_timetable.route_id,
                "start_stop_id": new_timetable.start_stop_id,
                "weekday": new_timetable.weekdays,
                "departure_time": new_timetable.departure_time.replace(tzinfo=KST),
            },
        )
        .returning(BusTimetable)
    )
    return await fetch_one(insert_query)


async def delete_timetable(
    route_id: int,
    start_stop_id: int,
    weekday: str,
    departure_time: datetime.time,
) -> None:
    delete_query = delete(BusTimetable).where(
        BusTimetable.route_id == route_id,
        BusTimetable.start_stop_id == start_stop_id,
        BusTimetable.weekday == weekday,
        BusTimetable.departure_time == departure_time,
    )
    await execute_query(delete_query)


async def list_realtime() -> list[dict[str, Any]]:
    select_query = select(BusRealtime)
    return await fetch_all(select_query)


async def list_realtime_filter(
    route_id: int | None = None,
    stop_id: int | None = None,
) -> list[dict[str, Any]]:
    conditions = []
    if route_id is not None:
        conditions.append(BusRealtime.route_id == route_id)
    if stop_id is not None:
        conditions.append(BusRealtime.stop_id == stop_id)
    select_query = select(BusRealtime).where(*conditions)
    return await fetch_all(select_query)
