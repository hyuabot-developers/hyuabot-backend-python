import datetime

from shuttle import service
from shuttle.exceptions import (
    DuplicateHolidayDate,
    TimetableNotFound,
    RouteNotFound,
    StopNotFound,
    RouteStopNotFound,
    DuplicateStopName,
    DuplicateRouteStop,
    DuplicateRouteName,
    PeriodNotFound,
    DuplicatePeriod,
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
        new_period.type,
        datetime.datetime.combine(new_period.start, datetime.time.min, tzinfo=KST),
        datetime.datetime.combine(new_period.end, datetime.time.max, tzinfo=KST),
    ):
        raise DuplicatePeriod()
    return new_period


async def get_valid_period(
    period_type_name: str,
    start: datetime.datetime,
    end: datetime.datetime,
) -> str:
    if await service.get_period(period_type_name, start, end) is None:
        raise PeriodNotFound()
    return period_type_name


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
    new_route_stop: CreateShuttleRouteStopRequest,
) -> CreateShuttleRouteStopRequest:
    if await service.get_route_stop(
        new_route_stop.route_name,
        new_route_stop.stop_name,
    ):
        raise DuplicateRouteStop()
    return new_route_stop


async def get_valid_route_stop(route_name: str, stop_name: str) -> str:
    if await service.get_route_stop(route_name, stop_name) is None:
        raise RouteStopNotFound()
    return route_name


async def create_valid_timetable(
    new_timetable: CreateShuttleTimetableRequest,
) -> CreateShuttleTimetableRequest:
    if await service.get_route(new_timetable.route_name) is None:
        raise RouteNotFound()
    return new_timetable


async def get_valid_timetable(seq: int) -> int:
    if await service.get_timetable(seq) is None:
        raise TimetableNotFound()
    return seq
