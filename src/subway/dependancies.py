from subway import service
from subway.exceptions import (
    DuplicateStationName,
    StationNameNotFound,
    DuplicateRouteID,
    RouteNotFound,
    DuplicateStationID,
    StationNotFound,
    DuplicateTimetable,
)
from subway.schemas import (
    CreateSubwayStation,
    CreateSubwayRoute,
    CreateSubwayRouteStation,
    CreateSubwayTimetable,
)
from utils import KST


async def create_valid_station(new_station: CreateSubwayStation) -> CreateSubwayStation:
    if await service.get_station_name(new_station.name):
        raise DuplicateStationName()

    return new_station


async def delete_valid_station(station_name: str) -> str:
    if await service.get_station_name(station_name) is None:
        raise StationNameNotFound()

    return station_name


async def create_valid_route(new_route: CreateSubwayRoute) -> CreateSubwayRoute:
    if await service.get_route(new_route.id):
        raise DuplicateRouteID()

    return new_route


async def get_valid_route(route_id: int) -> int:
    if await service.get_route(route_id) is None:
        raise RouteNotFound()

    return route_id


async def get_valid_route_station(station_id: str) -> str:
    if await service.get_route_station(station_id) is None:
        raise StationNotFound()

    return station_id


async def create_valid_route_station(
    new_station: CreateSubwayRouteStation,
) -> CreateSubwayRouteStation:
    if await service.get_route(new_station.route_id) is None:
        raise RouteNotFound()

    if await service.get_station_name(new_station.name) is None:
        raise StationNameNotFound()

    if await service.get_route_station(new_station.id):
        raise DuplicateStationID()

    return new_station


async def create_valid_timetable(
    station_id: str,
    new_timetable: CreateSubwayTimetable,
) -> CreateSubwayTimetable:
    if await service.get_timetable(
        station_id,
        new_timetable.weekday,
        new_timetable.heading,
        new_timetable.departure_time.replace(tzinfo=KST),
    ):
        raise DuplicateTimetable()

    return new_timetable
