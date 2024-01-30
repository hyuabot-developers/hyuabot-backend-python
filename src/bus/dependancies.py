from bus import service
from bus.exceptions import (
    DuplicateTimetable,
    StartStopNotFound,
    RouteNotFound,
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
from utils import KST


async def create_valid_route(new_route: CreateBusRouteRequest) -> CreateBusRouteRequest:
    if await service.get_route(new_route.id_):
        raise DuplicateRouteID()
    return new_route


async def get_valid_route(route_id: int) -> int:
    if await service.get_route(route_id) is None:
        raise RouteNotFound()
    return route_id


async def create_valid_stop(new_stop: CreateBusStopRequest) -> CreateBusStopRequest:
    if await service.get_stop(new_stop.id_):
        raise DuplicateStopID()
    return new_stop


async def get_valid_stop(stop_id: int) -> int:
    if await service.get_stop(stop_id) is None:
        raise StopNotFound()
    return stop_id


async def create_valid_route_stop(
    new_route_stop: CreateBusRouteStopRequest,
) -> CreateBusRouteStopRequest:
    if await service.get_stop(new_route_stop.stop_id) is None:
        raise StopNotFound()
    return new_route_stop


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
            new_timetable.departure_time.replace(tzinfo=KST),
        )
        is not None
    ):
        raise DuplicateTimetable()
    return new_timetable
