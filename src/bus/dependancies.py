import datetime

from bus import service
from bus.exceptions import (
    TimetableNotFound,
    DuplicateTimetable,
    StartStopNotFound,
    RouteNotFound,
    RouteStopNotFound,
    DuplicateRouteStop,
    StopNotFound,
    DuplicateStopID,
    DuplicateRouteID,
)
from bus.schemas import (
    CreateBusRouteRequest,
    CreateBusStopRequest,
    CreateBusRouteStopRequest,
    CreateBusTimetableRequest,
)


async def create_valid_route(new_route: CreateBusRouteRequest) -> CreateBusRouteRequest:
    if await service.get_route(new_route.id):
        raise DuplicateRouteID()
    return new_route


async def get_valid_route(route_id: int) -> int:
    if await service.get_route(route_id) is None:
        raise RouteNotFound()
    return route_id


async def create_valid_stop(new_stop: CreateBusStopRequest) -> CreateBusStopRequest:
    if await service.get_stop(new_stop.id):
        raise DuplicateStopID()
    return new_stop


async def get_valid_stop(stop_id: int) -> int:
    if await service.get_stop(stop_id) is None:
        raise StopNotFound()
    return stop_id


async def create_valid_route_stop(
    new_route_stop: CreateBusRouteStopRequest,
) -> CreateBusRouteStopRequest:
    if await service.get_route(new_route_stop.route_id) is None:
        raise RouteNotFound()
    elif await service.get_stop(new_route_stop.stop_id) is None:
        raise StopNotFound()
    elif await service.get_route_stop(
        new_route_stop.route_id,
        new_route_stop.stop_id,
    ):
        raise DuplicateRouteStop()
    return new_route_stop


async def get_valid_route_stop(route_id: int, stop_id: int) -> int:
    if await service.get_route_stop(route_id, stop_id) is None:
        raise RouteStopNotFound()
    return route_id


async def create_valid_timetable(
    new_timetable: CreateBusTimetableRequest,
) -> CreateBusTimetableRequest:
    if await service.get_route(new_timetable.route_id) is None:
        raise RouteNotFound()
    elif await service.get_stop(new_timetable.start_stop_id) is None:
        raise StartStopNotFound()
    elif (
        await service.get_timetable(
            new_timetable.route_id,
            new_timetable.start_stop_id,
            new_timetable.weekdays,
            new_timetable.departure_time,
        )
        is not None
    ):
        raise DuplicateTimetable()
    return new_timetable


async def get_valid_timetable(
    route_id: int,
    start_stop_id: int,
    weekday: str,
    departure_time: datetime.time,
) -> int:
    if (
        await service.get_timetable(
            route_id,
            start_stop_id,
            weekday,
            departure_time,
        )
        is None
    ):
        raise TimetableNotFound()
    return route_id
