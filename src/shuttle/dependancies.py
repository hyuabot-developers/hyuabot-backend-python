import datetime

from shuttle import service
from shuttle.exceptions import (
    DuplicateHolidayDate,
    TimetableNotFound,
    RouteNotFound,
    StopNotFound,
    DuplicateStopName,
    DuplicateRouteStop,
    DuplicateRouteName,
    DuplicatePeriod,
    DuplicateTimetable,
)
from shuttle.schemas import (
    CreateShuttleHolidayRequest,
    CreateShuttlePeriodRequest,
    CreateShuttleRouteRequest,
    CreateShuttleStopRequest,
    CreateShuttleRouteStopRequest,
    CreateShuttleTimetableRequest,
)
from utils import KST


async def create_valid_holiday(
    new_holiday: CreateShuttleHolidayRequest,
) -> CreateShuttleHolidayRequest:
    if await service.get_holiday(new_holiday.calendar, new_holiday.date):
        raise DuplicateHolidayDate()
    return new_holiday


async def create_valid_period(
    new_period: CreateShuttlePeriodRequest,
) -> CreateShuttlePeriodRequest:
    if await service.get_period(
        new_period.type_,
        datetime.datetime.combine(
            new_period.start,
            datetime.time(0, 0, 0),
            tzinfo=KST,
        ),
        datetime.datetime.combine(
            new_period.end,
            datetime.time(23, 59, 59),
            tzinfo=KST,
        ),
    ):
        raise DuplicatePeriod()
    return new_period


async def create_valid_route(
    new_route: CreateShuttleRouteRequest,
) -> CreateShuttleRouteRequest:
    if await service.get_route(new_route.name):
        raise DuplicateRouteName()
    return new_route


async def get_valid_route(route_name: str) -> str:
    if await service.get_route(route_name) is None:
        raise RouteNotFound()
    return route_name


async def create_valid_stop(
    new_stop: CreateShuttleStopRequest,
) -> CreateShuttleStopRequest:
    if await service.get_stop(new_stop.name):
        raise DuplicateStopName()
    return new_stop


async def get_valid_stop(stop_name: str) -> str:
    if await service.get_stop(stop_name) is None:
        raise StopNotFound()
    return stop_name


async def create_valid_route_stop(
    route_name: str,
    new_route_stop: CreateShuttleRouteStopRequest,
) -> CreateShuttleRouteStopRequest:
    if await service.get_route_stop(
        route_name,
        new_route_stop.stop_name,
    ):
        raise DuplicateRouteStop()
    return new_route_stop


async def create_valid_timetable(
    new_timetable: CreateShuttleTimetableRequest,
) -> CreateShuttleTimetableRequest:
    if await service.get_route(new_timetable.route_name) is None:
        raise RouteNotFound()
    elif (
        await service.get_timetable_by_filter(
            new_timetable.route_name,
            new_timetable.period_type,
            new_timetable.is_weekdays,
            new_timetable.departure_time,
        )
        is not None
    ):
        raise DuplicateTimetable()
    return new_timetable


async def get_valid_timetable(seq: int) -> int:
    if await service.get_timetable(seq) is None:
        raise TimetableNotFound()
    return seq
