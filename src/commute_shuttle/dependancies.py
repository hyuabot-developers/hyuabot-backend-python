from commute_shuttle import service
from commute_shuttle.exceptions import (
    DuplicateRouteName,
    RouteNotFound,
    StopNotFound,
    DuplicateStopName,
    DuplicateTimetableSequence,
)
from commute_shuttle.schemas import (
    CreateCommuteShuttleRouteRequest,
    CreateCommuteShuttleStopRequest,
    CreateCommuteShuttleTimetableRequest,
)


async def create_valid_route(
    new_route: CreateCommuteShuttleRouteRequest,
) -> CreateCommuteShuttleRouteRequest:
    if await service.get_route(new_route.name):
        raise DuplicateRouteName()
    return new_route


async def get_valid_route(route_name: str) -> str:
    if await service.get_route(route_name) is None:
        raise RouteNotFound()
    return route_name


async def create_valid_stop(
    new_stop: CreateCommuteShuttleStopRequest,
) -> CreateCommuteShuttleStopRequest:
    if await service.get_stop(new_stop.name):
        raise DuplicateStopName()
    return new_stop


async def get_valid_stop(stop_id: str) -> str:
    if await service.get_stop(stop_id) is None:
        raise StopNotFound()
    return stop_id


async def create_valid_timetable(
    new_timetable: CreateCommuteShuttleTimetableRequest,
) -> CreateCommuteShuttleTimetableRequest:
    if await service.get_route(new_timetable.route_name) is None:
        raise RouteNotFound()
    elif await service.get_stop(new_timetable.stop_name) is None:
        raise StopNotFound()
    elif await service.get_timetable_filter(
        new_timetable.route_name,
        new_timetable.sequence,
    ):
        raise DuplicateTimetableSequence()
    return new_timetable


async def get_valid_timetable(
    route_name: str,
    stop_name: str,
) -> tuple[str, str]:
    if await service.get_timetable(route_name, stop_name) is None:
        raise StopNotFound()
    return route_name, stop_name
