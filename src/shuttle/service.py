import datetime
from typing import Any

from sqlalchemy import select, insert, delete, update, true

from database import fetch_one, fetch_all, execute_query
from model.shuttle import (
    ShuttleHoliday,
    ShuttlePeriod,
    ShuttleRoute,
    ShuttleStop,
    ShuttleRouteStop,
    ShuttleTimetable,
    ShuttleTimetableView,
)
from shuttle.schemas import (
    CreateShuttleHolidayRequest,
    CreateShuttlePeriodRequest,
    CreateShuttleRouteRequest,
    UpdateShuttleRouteRequest,
    CreateShuttleStopRequest,
    CreateShuttleRouteStopRequest,
    UpdateShuttleRouteStopRequest,
    CreateShuttleTimetableRequest,
    UpdateShuttleTimetableRequest,
    UpdateShuttleStopRequest,
)
from utils import KST


async def list_holiday() -> list[dict[str, str]]:
    select_query = select(ShuttleHoliday)
    return await fetch_all(select_query)


async def list_holiday_filter(
    calendar_type: str | None = None,
    date: datetime.date | None = None,
    start_date: datetime.date | None = None,
    end_date: datetime.date | None = None,
):
    conditions = []
    if calendar_type:
        conditions.append(ShuttleHoliday.calendar == calendar_type)
    if date:
        conditions.append(ShuttleHoliday.date == date)
    if start_date:
        conditions.append(ShuttleHoliday.date >= start_date)
    if end_date:
        conditions.append(ShuttleHoliday.date <= end_date)

    select_query = select(ShuttleHoliday).where(*conditions)
    return await fetch_all(select_query)


async def get_holiday(calendar_type: str, date: datetime.date) -> dict[str, str] | None:
    select_query = select(ShuttleHoliday).where(
        ShuttleHoliday.calendar == calendar_type,
        ShuttleHoliday.date == date,
    )
    return await fetch_one(select_query)


async def create_holiday(
    new_holiday: CreateShuttleHolidayRequest,
) -> dict[str, str] | None:
    insert_query = (
        insert(ShuttleHoliday)
        .values(
            {
                "holiday_date": new_holiday.date,
                "holiday_type": new_holiday.type,
                "calendar_type": new_holiday.calendar,
            },
        )
        .returning(ShuttleHoliday)
    )
    return await fetch_one(insert_query)


async def delete_holiday(calendar_type: str, date: datetime.date) -> None:
    delete_query = delete(ShuttleHoliday).where(
        ShuttleHoliday.calendar == calendar_type,
        ShuttleHoliday.date == date,
    )
    await execute_query(delete_query)


async def list_period() -> list[dict[str, str]]:
    select_query = select(ShuttlePeriod)
    return await fetch_all(select_query)


async def list_period_filter(
    period_type: str | None = None,
    date: datetime.date | None = None,
):
    conditions = []
    if period_type:
        conditions.append(ShuttlePeriod.type_id == period_type)
    if date:
        conditions.append(ShuttlePeriod.start <= date)
        conditions.append(ShuttlePeriod.end >= date)

    select_query = select(ShuttlePeriod).where(*conditions)
    return await fetch_all(select_query)


async def get_period(
    period_type: str,
    start: datetime.datetime,
    end: datetime.datetime,
) -> dict[str, str] | None:
    select_query = select(ShuttlePeriod).where(
        ShuttlePeriod.type_id == period_type,
        ShuttlePeriod.start == start,
        ShuttlePeriod.end == end,
    )
    return await fetch_one(select_query)


async def create_period(
    new_period: CreateShuttlePeriodRequest,
) -> dict[str, str] | None:
    insert_query = (
        insert(ShuttlePeriod)
        .values(
            {
                "period_type": new_period.type,
                "period_start": datetime.datetime.strptime(
                    f"{new_period.start}T00:00:00+09:00",
                    "%Y-%m-%dT%H:%M:%S%z",
                ),
                "period_end": datetime.datetime.strptime(
                    f"{new_period.end}T23:59:59+09:00",
                    "%Y-%m-%dT%H:%M:%S%z",
                ),
            },
        )
        .returning(ShuttlePeriod)
    )
    return await fetch_one(insert_query)


async def delete_period(
    period_type: str,
    start: datetime.date,
    end: datetime.date,
) -> None:
    start_datetime = datetime.datetime.strptime(
        f"{start}T00:00:00+09:00",
        "%Y-%m-%dT%H:%M:%S%z",
    )
    end_datetime = datetime.datetime.strptime(
        f"{end}T23:59:59+09:00",
        "%Y-%m-%dT%H:%M:%S%z",
    )
    delete_query = delete(ShuttlePeriod).where(
        ShuttlePeriod.type_id == period_type,
        ShuttlePeriod.start == start_datetime,
        ShuttlePeriod.end == end_datetime,
    )
    await execute_query(delete_query)


async def list_route() -> list[dict[str, str]]:
    select_query = select(ShuttleRoute)
    return await fetch_all(select_query)


async def list_route_filter(
    name: str | None = None,
    tag: str | None = None,
):
    conditions = []
    if name:
        conditions.append(ShuttleRoute.name == name)
    if tag:
        conditions.append(ShuttleRoute.tag == tag)

    select_query = select(ShuttleRoute).where(*conditions)
    return await fetch_all(select_query)


async def get_route(route_name: str) -> dict[str, str] | None:
    select_query = select(ShuttleRoute).where(ShuttleRoute.name == route_name)
    return await fetch_one(select_query)


async def create_route(
    new_route: CreateShuttleRouteRequest,
) -> dict[str, str] | None:
    insert_query = (
        insert(ShuttleRoute)
        .values(
            {
                "route_name": new_route.name,
                "route_tag": new_route.tag,
                "route_description_korean": new_route.route_description_korean,
                "route_description_english": new_route.route_description_english,
                "start_stop_id": new_route.start_stop_id,
                "end_stop_id": new_route.end_stop_id,
            },
        )
        .returning(ShuttleRoute)
    )
    return await fetch_one(insert_query)


async def update_route(
    route_name: str,
    new_route: UpdateShuttleRouteRequest,
) -> dict[str, str] | None:
    update_query = (
        update(ShuttleRoute)
        .where(ShuttleRoute.name == route_name)
        .values(
            {
                "route_tag": new_route.tag,
                "route_description_korean": new_route.route_description_korean,
                "route_description_english": new_route.route_description_english,
                "start_stop_id": new_route.start_stop_id,
                "end_stop_id": new_route.end_stop_id,
            },
        )
        .returning(ShuttleRoute)
    )
    return await fetch_one(update_query)


async def delete_route(route_name: str) -> None:
    delete_query = delete(ShuttleRoute).where(ShuttleRoute.name == route_name)
    await execute_query(delete_query)


async def list_stop() -> list[dict[str, str]]:
    select_query = select(ShuttleStop)
    return await fetch_all(select_query)


async def list_stop_filter(name: str):
    select_query = select(ShuttleStop).where(
        ShuttleStop.name == name,
    )
    return await fetch_all(select_query)


async def get_stop(stop_name: str) -> dict[str, str] | None:
    select_query = select(ShuttleStop).where(ShuttleStop.name == stop_name)
    return await fetch_one(select_query)


async def create_stop(
    new_stop: CreateShuttleStopRequest,
) -> dict[str, str] | None:
    insert_query = (
        insert(ShuttleStop)
        .values(
            {
                "stop_name": new_stop.name,
                "latitude": new_stop.latitude,
                "longitude": new_stop.longitude,
            },
        )
        .returning(ShuttleStop)
    )
    return await fetch_one(insert_query)


async def update_stop(
    stop_name: str,
    new_stop: UpdateShuttleStopRequest,
) -> dict[str, str] | None:
    update_query = (
        update(ShuttleStop)
        .where(ShuttleStop.name == stop_name)
        .values(
            {
                "latitude": new_stop.latitude,
                "longitude": new_stop.longitude,
            },
        )
        .returning(ShuttleStop)
    )
    return await fetch_one(update_query)


async def delete_stop(stop_name: str) -> None:
    delete_query = delete(ShuttleStop).where(ShuttleStop.name == stop_name)
    await execute_query(delete_query)


async def list_route_stop_filter(
    route_name: str,
):
    select_query = select(ShuttleRouteStop).where(
        ShuttleRouteStop.route_name == route_name,
    )
    return await fetch_all(select_query)


async def get_route_stop(
    route_name: str,
    stop_name: str,
) -> dict[str, Any] | None:
    select_query = select(ShuttleRouteStop).where(
        ShuttleRouteStop.route_name == route_name,
        ShuttleRouteStop.stop_name == stop_name,
    )
    return await fetch_one(select_query)


async def create_route_stop(
    route_name: str,
    new_route_stop: CreateShuttleRouteStopRequest,
) -> dict[str, Any] | None:
    insert_query = (
        insert(ShuttleRouteStop)
        .values(
            {
                "route_name": route_name,
                "stop_name": new_route_stop.stop_name,
                "stop_order": new_route_stop.sequence,
                "cumulative_time": new_route_stop.cumulative_time,
            },
        )
        .returning(ShuttleRouteStop)
    )
    return await fetch_one(insert_query)


async def update_route_stop(
    route_name: str,
    stop_name: str,
    new_route_stop: UpdateShuttleRouteStopRequest,
) -> dict[str, Any] | None:
    update_query = (
        update(ShuttleRouteStop)
        .where(
            ShuttleRouteStop.route_name == route_name,
            ShuttleRouteStop.stop_name == stop_name,
        )
        .values(
            {
                "stop_order": new_route_stop.sequence,
                "cumulative_time": new_route_stop.cumulative_time,
            },
        )
        .returning(ShuttleRouteStop)
    )
    return await fetch_one(update_query)


async def delete_route_stop(
    route_name: str,
    stop_name: str,
) -> None:
    delete_query = delete(ShuttleRouteStop).where(
        ShuttleRouteStop.route_name == route_name,
        ShuttleRouteStop.stop_name == stop_name,
    )
    await execute_query(delete_query)


async def list_timetable() -> list[dict[str, str]]:
    select_query = select(ShuttleTimetable)
    return await fetch_all(select_query)


async def list_timetable_filter(
    route: str | None = None,
    weekdays: bool | None = None,
    start_time: datetime.time | None = None,
    end_time: datetime.time | None = None,
):
    conditions = []
    if route:
        conditions.append(ShuttleTimetable.route_name == route)
    if weekdays is True:
        conditions.append(ShuttleTimetable.is_weekdays.is_(true()))
    elif weekdays is False:
        conditions.append(ShuttleTimetable.is_weekdays.isnot(true()))
    if start_time:
        conditions.append(
            ShuttleTimetable.departure_time >= start_time.replace(tzinfo=KST),
        )
    if end_time:
        conditions.append(
            ShuttleTimetable.departure_time <= end_time.replace(tzinfo=KST),
        )
    select_query = select(ShuttleTimetable).where(*conditions)
    return await fetch_all(select_query)


async def get_timetable(seq: int) -> dict[str, str] | None:
    select_query = select(ShuttleTimetable).where(ShuttleTimetable.id == seq)
    return await fetch_one(select_query)


async def get_timetable_by_filter(
    route_name: str,
    period_type: str,
    is_weekdays: bool,
    departure_time: datetime.time,
) -> dict[str, str] | None:
    select_query = select(ShuttleTimetable).where(
        ShuttleTimetable.route_name == route_name,
        ShuttleTimetable.period == period_type,
        ShuttleTimetable.is_weekdays == is_weekdays,
        ShuttleTimetable.departure_time == departure_time.replace(tzinfo=KST),
    )
    return await fetch_one(select_query)


async def create_timetable(
    new_timetable: CreateShuttleTimetableRequest,
) -> dict[str, Any] | None:
    insert_query = (
        insert(ShuttleTimetable)
        .values(
            {
                "period_type": new_timetable.period_type,
                "weekday": new_timetable.is_weekdays,
                "route_name": new_timetable.route_name,
                "departure_time": new_timetable.departure_time.replace(
                    tzinfo=KST,
                ),
            },
        )
        .returning(ShuttleTimetable)
    )
    return await fetch_one(insert_query)


async def update_timetable(
    seq: int,
    new_timetable: UpdateShuttleTimetableRequest,
) -> dict[str, str] | None:
    update_query = (
        update(ShuttleTimetable)
        .where(ShuttleTimetable.id == seq)
        .values(
            {
                "period_type": new_timetable.period_type,
                "weekday": new_timetable.is_weekdays,
                "route_name": new_timetable.route_name,
                "departure_time": (
                    new_timetable.departure_time.replace(
                        tzinfo=KST,
                    )
                    if new_timetable.departure_time
                    else None
                ),
            },
        )
        .returning(ShuttleTimetable)
    )
    return await fetch_one(update_query)


async def delete_timetable(seq: int) -> None:
    delete_query = delete(ShuttleTimetable).where(ShuttleTimetable.id == seq)
    await execute_query(delete_query)


async def list_timetable_view() -> list[dict[str, str]]:
    select_query = select(ShuttleTimetableView)
    return await fetch_all(select_query)


async def list_timetable_view_filter(
    route: str | None = None,
    stop: str | None = None,
    weekdays: bool | None = None,
    start_time: datetime.time | None = None,
    end_time: datetime.time | None = None,
):
    conditions = []
    if route:
        conditions.append(ShuttleTimetableView.route_name == route)
    if stop:
        conditions.append(ShuttleTimetableView.stop_name == stop)
    if weekdays is True:
        conditions.append(ShuttleTimetableView.is_weekdays.is_(true()))
    elif weekdays is False:
        conditions.append(ShuttleTimetableView.is_weekdays.isnot(true()))
    if start_time:
        start_time = start_time.replace(tzinfo=KST)
        conditions.append(ShuttleTimetableView.departure_time >= start_time)
    if end_time:
        end_time = end_time.replace(tzinfo=KST)
        conditions.append(ShuttleTimetableView.departure_time <= end_time)
    select_query = select(ShuttleTimetableView).where(*conditions)
    return await fetch_all(select_query)
