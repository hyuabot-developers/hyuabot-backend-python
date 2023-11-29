import datetime

from fastapi import APIRouter, Depends
from starlette import status

from exceptions import DetailedHTTPException
from subway import service
from subway.dependancies import (
    create_valid_station,
    delete_valid_station,
    create_valid_route,
    get_valid_route,
    create_valid_route_station,
    get_valid_route_station,
)
from subway.exceptions import (
    StationNameNotFound,
    StationNotFound,
    TimetableNotFound,
    RouteNotFound,
)
from subway.schemas import (
    SubwayStationListResponse,
    SubwayStationItemResponse,
    CreateSubwayStation,
    SubwayRouteListResponse,
    SubwayRouteItemResponse,
    CreateSubwayRoute,
    UpdateSubwayRoute,
    SubwayRouteStationListResponse,
    SubwayRouteStationDetailResponse,
    CreateSubwayRouteStation,
    UpdateSubwayRouteStation,
    SubwayTimetableListResponse,
    SubwayTimetableItemResponse,
    SubwayRealtimeListResponse,
    CreateSubwayTimetable,
)
from user.jwt import parse_jwt_user_data
from utils import timedelta_to_str, remove_timezone

router = APIRouter()


@router.get(
    "/station/name",
    status_code=status.HTTP_200_OK,
    response_model=SubwayStationListResponse,
)
async def get_station_name_list(
    _: str = Depends(parse_jwt_user_data),
    name: str | None = None,
):
    if name is None:
        data = await service.list_station_name()
    else:
        data = await service.list_station_name_filter(name)
    return {"data": map(lambda x: {"name": x["station_name"]}, data)}


@router.post(
    "/station/name",
    status_code=status.HTTP_201_CREATED,
    response_model=SubwayStationItemResponse,
)
async def create_station_name(
    payload: CreateSubwayStation = Depends(create_valid_station),
    _: str = Depends(parse_jwt_user_data),
):
    station = await service.create_station_name(payload)
    if station is None:
        raise DetailedHTTPException()
    return {"name": station["station_name"]}


@router.get(
    "/station/name/{station_name}",
    status_code=status.HTTP_200_OK,
    response_model=SubwayStationItemResponse,
)
async def get_station_name(
    station_name: str,
    _: str = Depends(parse_jwt_user_data),
):
    station = await service.get_station_name(station_name)
    if station is None:
        raise StationNameNotFound()
    return {"name": station["station_name"]}


@router.delete(
    "/station/name/{station_name}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_station_name(
    station_name: str = Depends(delete_valid_station),
    _: str = Depends(parse_jwt_user_data),
):
    return await service.delete_station_name(station_name)


@router.get(
    "/route",
    status_code=status.HTTP_200_OK,
    response_model=SubwayRouteListResponse,
)
async def get_route_list(
    _: str = Depends(parse_jwt_user_data),
    name: str | None = None,
):
    if name is None:
        data = await service.list_route()
    else:
        data = await service.list_route_filter(name)
    return {
        "data": map(
            lambda x: {
                "name": x["route_name"],
                "id": x["route_id"],
            },
            data,
        ),
    }


@router.post(
    "/route",
    status_code=status.HTTP_201_CREATED,
    response_model=SubwayRouteItemResponse,
)
async def create_route(
    payload: CreateSubwayRoute = Depends(create_valid_route),
    _: str = Depends(parse_jwt_user_data),
):
    route = await service.create_route(payload)
    if route is None:
        raise DetailedHTTPException()
    return {
        "name": route["route_name"],
        "id": route["route_id"],
    }


@router.get(
    "/route/{route_id}",
    status_code=status.HTTP_200_OK,
    response_model=SubwayRouteItemResponse,
)
async def get_route(
    route_id: int = Depends(get_valid_route),
    _: str = Depends(parse_jwt_user_data),
):
    route = await service.get_route(route_id)
    if route is None:
        raise RouteNotFound()
    return {"name": route["route_name"], "id": route["route_id"]}


@router.patch(
    "/route/{route_id}",
    status_code=status.HTTP_200_OK,
    response_model=SubwayRouteItemResponse,
)
async def update_route(
    payload: UpdateSubwayRoute,
    route_id: int = Depends(get_valid_route),
    _: str = Depends(parse_jwt_user_data),
):
    await service.update_route(route_id, payload)
    route = await service.get_route(route_id)
    if route is None:
        raise DetailedHTTPException()
    return {"name": route["route_name"], "id": route["route_id"]}


@router.delete(
    "/route/{route_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_route(
    route_id: int = Depends(get_valid_route),
    _: str = Depends(parse_jwt_user_data),
):
    await service.delete_route(route_id)


@router.get(
    "/station",
    status_code=status.HTTP_200_OK,
    response_model=SubwayRouteStationListResponse,
)
async def get_route_station_list(
    _: str = Depends(parse_jwt_user_data),
    route: int | None = None,
):
    if route is None:
        data = await service.list_route_station()
    else:
        data = await service.list_route_station_filter(route)
    return {
        "data": map(
            lambda x: {
                "id": x["station_id"],
                "name": x["station_name"],
                "routeID": x["route_id"],
                "sequence": x["station_sequence"],
                "cumulativeTime": timedelta_to_str(
                    x["cumulative_time"],
                ),
            },
            data,
        ),
    }


@router.get(
    "/station/{station_id}",
    status_code=status.HTTP_200_OK,
    response_model=SubwayRouteStationDetailResponse,
)
async def get_route_station(
    station_id: str,
    _: str = Depends(parse_jwt_user_data),
):
    station = await service.get_route_station(station_id)
    if station is None:
        raise StationNotFound()
    return {
        "id": station["station_id"],
        "name": station["station_name"],
        "routeID": station["route_id"],
        "sequence": station["station_sequence"],
        "cumulativeTime": timedelta_to_str(
            station["cumulative_time"],
        ),
    }


@router.post(
    "/station",
    status_code=status.HTTP_201_CREATED,
    response_model=SubwayRouteStationDetailResponse,
)
async def create_route_station(
    payload: CreateSubwayRouteStation = Depends(create_valid_route_station),
    _: str = Depends(parse_jwt_user_data),
):
    station = await service.create_route_station(payload)
    if station is None:
        raise DetailedHTTPException()
    return {
        "id": station["station_id"],
        "name": station["station_name"],
        "routeID": station["route_id"],
        "sequence": station["station_sequence"],
        "cumulativeTime": timedelta_to_str(
            station["cumulative_time"],
        ),
    }


@router.patch(
    "/station/{station_id}",
    status_code=status.HTTP_200_OK,
    response_model=SubwayRouteStationDetailResponse,
)
async def update_route_station(
    payload: UpdateSubwayRouteStation,
    station_id: str = Depends(get_valid_route_station),
    _: str = Depends(parse_jwt_user_data),
):
    await service.update_route_station(station_id, payload)
    station = await service.get_route_station(station_id)
    if station is None:
        raise DetailedHTTPException()
    return {
        "id": station["station_id"],
        "name": station["station_name"],
        "routeID": station["route_id"],
        "sequence": station["station_sequence"],
        "cumulativeTime": timedelta_to_str(
            station["cumulative_time"],
        ),
    }


@router.delete(
    "/station/{station_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_route_station(
    station_id: str = Depends(get_valid_route_station),
    _: str = Depends(parse_jwt_user_data),
):
    await service.delete_route_station(station_id)


@router.get(
    "/station/{station_id}/timetable",
    status_code=status.HTTP_200_OK,
    response_model=SubwayTimetableListResponse,
)
async def get_route_station_timetable_list(
    station_id: str = Depends(get_valid_route_station),
    _: str = Depends(parse_jwt_user_data),
):
    timetable = await service.get_timetable_by_station(station_id)
    return {
        "data": map(
            lambda x: {
                "stationID": x["station_id"],
                "start_station_id": x["start_station_id"],
                "terminal_station_id": x["terminal_station_id"],
                "departureTime": remove_timezone(x["departure_time"]),
                "weekday": x["weekday"],
                "heading": x["up_down_type"],
            },
            timetable,
        ),
    }


@router.post(
    "/station/{station_id}/timetable",
    status_code=status.HTTP_201_CREATED,
    response_model=SubwayTimetableItemResponse,
)
async def create_route_station_timetable(
    payload: CreateSubwayTimetable,
    station_id: str = Depends(get_valid_route_station),
    _: str = Depends(parse_jwt_user_data),
):
    timetable = await service.create_timetable(station_id, payload)
    if timetable is None:
        raise DetailedHTTPException()
    return {
        "stationID": timetable["station_id"],
        "start_station_id": timetable["start_station_id"],
        "terminal_station_id": timetable["terminal_station_id"],
        "departureTime": remove_timezone(timetable["departure_time"]),
        "weekday": timetable["weekday"],
        "heading": timetable["up_down_type"],
    }


@router.get(
    "/station/{station_id}/timetable/{heading}/{weekday}/{departure_time}",
    status_code=status.HTTP_200_OK,
    response_model=SubwayTimetableItemResponse,
)
async def get_route_station_timetable(
    station_id: str,
    heading: str,
    weekday: str,
    departure_time: datetime.time,
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.get_timetable(
        station_id,
        weekday,
        heading,
        departure_time,
    )
    if data is None:
        raise TimetableNotFound()
    return {
        "stationID": data["station_id"],
        "start_station_id": data["start_station_id"],
        "terminal_station_id": data["terminal_station_id"],
        "departureTime": remove_timezone(data["departure_time"]),
        "weekday": data["weekday"],
        "heading": data["up_down_type"],
    }


@router.delete(
    "/station/{station_id}/timetable/{heading}/{weekday}/{departure_time}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_route_station_timetable(
    station_id: str,
    heading: str,
    weekday: str,
    departure_time: datetime.time,
    _: str = Depends(parse_jwt_user_data),
):
    await service.delete_timetable(
        station_id,
        weekday,
        heading,
        departure_time,
    )
    return {"message": "Hello World"}


@router.get(
    "/station/{station_id}/realtime",
    status_code=status.HTTP_200_OK,
    response_model=SubwayRealtimeListResponse,
)
async def get_route_station_realtime(
    station_id: str,
    _: str = Depends(parse_jwt_user_data),
):
    realtime = await service.get_realtime(station_id)
    return {
        "data": map(
            lambda x: {
                "stationID": x["station_id"],
                "sequence": x["arrival_sequence"],
                "current": x["current_station_name"],
                "heading": x["up_down_type"],
                "station": x["remaining_stop_count"],
                "time": timedelta_to_str(x["remaining_time"]),
                "trainNumber": x["train_number"],
                "express": x["is_express_train"],
                "last": x["is_last_train"],
                "terminalStationID": x["terminal_station_id"],
                "status": x["status_code"],
            },
            realtime,
        ),
    }
