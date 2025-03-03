import datetime
from typing import Callable

from fastapi import APIRouter, Depends
from starlette import status

from bus import service
from bus.dependancies import (
    get_valid_route,
    get_valid_stop,
    create_valid_route,
    create_valid_stop,
    create_valid_route_stop,
    create_valid_timetable,
)
from bus.exceptions import (
    RouteNotFound,
    StopNotFound,
    RouteStopNotFound,
    DuplicateRouteStop,
    TimetableNotFound,
)
from bus.schemas import (
    CreateBusRouteRequest,
    CreateBusStopRequest,
    CreateBusRouteStopRequest,
    CreateBusTimetableRequest,
    BusRouteListResponse,
    BusRouteDetailResponse,
    UpdateBusRouteRequest,
    BusStopListResponse,
    BusStopDetailResponse,
    UpdateBusStopRequest,
    BusRouteStopListResponse,
    BusRouteStopDetailResponse,
    UpdateBusRouteStopRequest,
    BusTimetableListResponse,
    BusTimetableDetailResponse,
    BusRealtimeListResponse,
)
from exceptions import DetailedHTTPException
from model.bus import BusRoute, BusStop, BusRouteStop, BusTimetable, BusRealtime
from user.jwt import parse_jwt_user_data
from utils import timestamp_tz_to_datetime, KST, datetime_to_str

router = APIRouter()


@router.get("/route", response_model=BusRouteListResponse)
async def get_bus_route_list(
    name: str | None = None,
    type_: str | None = None,
    company: str | None = None,
    _: str = Depends(parse_jwt_user_data),
):
    if name is None and type_ is None and company is None:
        data = await service.list_routes()
    else:
        data = await service.list_routes_filter(name, type_, company)
    mapping_func: Callable[[BusRoute], dict[str, int | str]] = lambda x: {
        "id": x.id_,
        "name": x.name,
        "type": x.type_name,
    }
    return {"data": map(mapping_func, data)}


@router.get("/route/{route_id}", response_model=BusRouteDetailResponse)
async def get_bus_route_detail(
    route_id: int,
    _: str = Depends(parse_jwt_user_data),
):
    route = await service.get_route(route_id)
    if route is None:
        raise RouteNotFound()
    return {
        "id": route.id_,
        "name": route.name,
        "type": route.type_name,
        "start": route.start_stop_id,
        "end": route.end_stop_id,
        "company": {
            "id": route.company_id,
            "name": route.company_name,
            "telephone": route.company_telephone,
        },
        "up": {
            "first": route.up_first_time,
            "last": route.up_last_time,
        },
        "down": {
            "first": route.down_first_time,
            "last": route.down_last_time,
        },
    }


@router.post(
    "/route",
    status_code=status.HTTP_201_CREATED,
    response_model=BusRouteDetailResponse,
)
async def create_bus_route(
    new_route: CreateBusRouteRequest = Depends(create_valid_route),
    _: str = Depends(parse_jwt_user_data),
):
    route = await service.create_route(new_route)
    if route is None:
        raise DetailedHTTPException()
    return {
        "id": route.id_,
        "name": route.name,
        "type": route.type_name,
        "start": route.start_stop_id,
        "end": route.end_stop_id,
        "company": {
            "id": route.company_id,
            "name": route.company_name,
            "telephone": route.company_telephone,
        },
        "up": {
            "first": route.up_first_time,
            "last": route.up_last_time,
        },
        "down": {
            "first": route.down_first_time,
            "last": route.down_last_time,
        },
    }


@router.patch("/route/{route_id}", response_model=BusRouteDetailResponse)
async def update_bus_route(
    payload: UpdateBusRouteRequest,
    route_id: int = Depends(get_valid_route),
    _: str = Depends(parse_jwt_user_data),
):
    route = await service.update_route(route_id, payload)
    if route is None:
        raise DetailedHTTPException()
    return {
        "id": route.id_,
        "name": route.name,
        "type": route.type_name,
        "start": route.start_stop_id,
        "end": route.end_stop_id,
        "company": {
            "id": route.company_id,
            "name": route.company_name,
            "telephone": route.company_telephone,
        },
        "up": {
            "first": route.up_first_time,
            "last": route.up_last_time,
        },
        "down": {
            "first": route.down_first_time,
            "last": route.down_last_time,
        },
    }


@router.delete("/route/{route_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bus_route(
    route_id: int = Depends(get_valid_route),
    _: str = Depends(parse_jwt_user_data),
):
    await service.delete_route(route_id)
    return None


@router.get("/stop", response_model=BusStopListResponse)
async def get_bus_stop_list(
    name: str | None = None,
    _: str = Depends(parse_jwt_user_data),
):
    if name is None:
        stops = await service.list_stops()
    else:
        stops = await service.list_stops_filter(name)
    mapping_func: Callable[[BusStop], dict[str, int | str]] = lambda x: {
        "id": x.id_,
        "name": x.name,
    }
    return {"data": map(mapping_func, stops)}


@router.get("/stop/{stop_id}", response_model=BusStopDetailResponse)
async def get_bus_stop_detail(
    stop_id: int,
    _: str = Depends(parse_jwt_user_data),
):
    stop = await service.get_stop(stop_id)
    if stop is None:
        raise StopNotFound()
    return {
        "id": stop.id_,
        "name": stop.name,
        "latitude": stop.latitude,
        "longitude": stop.longitude,
        "district": stop.district,
        "mobileNumber": stop.mobile_no,
        "regionName": stop.region,
    }


@router.post(
    "/stop",
    status_code=status.HTTP_201_CREATED,
    response_model=BusStopDetailResponse,
)
async def create_bus_stop(
    new_stop: CreateBusStopRequest = Depends(create_valid_stop),
    _: str = Depends(parse_jwt_user_data),
):
    stop = await service.create_stop(new_stop)
    if stop is None:
        raise DetailedHTTPException()
    return {
        "id": stop.id_,
        "name": stop.name,
        "latitude": stop.latitude,
        "longitude": stop.longitude,
        "district": stop.district,
        "mobileNumber": stop.mobile_no,
        "regionName": stop.region,
    }


@router.patch("/stop/{stop_id}", response_model=BusStopDetailResponse)
async def update_bus_stop(
    payload: UpdateBusStopRequest,
    stop_id: int = Depends(get_valid_stop),
    _: str = Depends(parse_jwt_user_data),
):
    stop = await service.update_stop(stop_id, payload)
    if stop is None:
        raise DetailedHTTPException()
    return {
        "id": stop.id_,
        "name": stop.name,
        "latitude": stop.latitude,
        "longitude": stop.longitude,
        "district": stop.district,
        "mobileNumber": stop.mobile_no,
        "regionName": stop.region,
    }


@router.delete("/stop/{stop_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bus_stop(
    stop_id: int = Depends(get_valid_stop),
    _: str = Depends(parse_jwt_user_data),
):
    await service.delete_stop(stop_id)
    return None


@router.get("/route-stop", response_model=BusRouteStopListResponse)
async def get_bus_route_stop_list(_: str = Depends(parse_jwt_user_data)):
    route_stops = await service.list_route_stops()
    mapping_func: Callable[[BusRouteStop], dict[str, int]] = lambda x: {
        "id": x.stop_id,
        "sequence": x.sequence,
        "start": x.start_stop_id,
        "minuteFromStart": x.minute_from_start,
    }
    return {"data": map(mapping_func, route_stops)}


@router.get("/route/{route_id}/stop", response_model=BusRouteStopListResponse)
async def get_bus_route_stop_list_filter(
    route_id: int = Depends(get_valid_route),
    _: str = Depends(parse_jwt_user_data),
):
    route_stops = await service.list_route_stops(route_id)
    mapping_func: Callable[[BusRouteStop], dict[str, int]] = lambda x: {
        "id": x.stop_id,
        "sequence": x.sequence,
        "start": x.start_stop_id,
        "minuteFromStart": x.minute_from_start,
    }
    return {"data": map(mapping_func, route_stops)}


@router.get(
    "/route/{route_id}/stop/{stop_id}",
    response_model=BusRouteStopDetailResponse,
)
async def get_bus_route_stop_detail(
    route_id: int = Depends(get_valid_route),
    stop_id: int = Depends(get_valid_stop),
    _: str = Depends(parse_jwt_user_data),
):
    route_stop = await service.get_route_stop(route_id, stop_id)
    if route_stop is None:
        raise RouteStopNotFound()
    return {
        "id": route_stop.stop_id,
        "sequence": route_stop.sequence,
        "start": route_stop.start_stop_id,
        "minuteFromStart": route_stop.minute_from_start,
    }


@router.post(
    "/route/{route_id}/stop",
    status_code=status.HTTP_201_CREATED,
    response_model=BusRouteStopDetailResponse,
)
async def create_bus_route_stop(
    route_id: int = Depends(get_valid_route),
    new_route_stop: CreateBusRouteStopRequest = Depends(create_valid_route_stop),
    _: str = Depends(parse_jwt_user_data),
):
    if await service.get_route_stop(route_id, new_route_stop.stop_id) is not None:
        raise DuplicateRouteStop()
    route_stop = await service.create_route_stop(route_id, new_route_stop)
    if route_stop is None:
        raise DetailedHTTPException()
    return {
        "id": route_stop.stop_id,
        "sequence": route_stop.sequence,
        "start": route_stop.start_stop_id,
        "minuteFromStart": route_stop.minute_from_start,
    }


@router.patch(
    "/route/{route_id}/stop/{stop_id}",
    response_model=BusRouteStopDetailResponse,
)
async def update_bus_route_stop(
    payload: UpdateBusRouteStopRequest,
    route_id: int = Depends(get_valid_route),
    stop_id: int = Depends(get_valid_stop),
    _: str = Depends(parse_jwt_user_data),
):
    route_stop = await service.update_route_stop(route_id, stop_id, payload)
    if route_stop is None:
        raise RouteStopNotFound()
    return {
        "id": route_stop.stop_id,
        "sequence": route_stop.sequence,
        "start": route_stop.start_stop_id,
        "minuteFromStart": route_stop.minute_from_start,
    }


@router.delete(
    "/route/{route_id}/stop/{stop_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_bus_route_stop(
    route_id: int = Depends(get_valid_route),
    stop_id: int = Depends(get_valid_stop),
    _: str = Depends(parse_jwt_user_data),
):
    if await service.get_route_stop(route_id, stop_id) is None:
        raise RouteStopNotFound()
    await service.delete_route_stop(route_id, stop_id)
    return None


@router.get("/timetable", response_model=BusTimetableListResponse)
async def get_bus_timetable_list(
    route_id: int | None = None,
    start_stop_id: int | None = None,
    weekdays: str | None = None,
    start: datetime.time | None = None,
    end: datetime.time | None = None,
    _: str = Depends(parse_jwt_user_data),
):
    if (
        route_id is None
        and start_stop_id is None
        and weekdays is None
        and start is None
        and end is None
    ):
        timetables = await service.list_timetable()
    else:
        timetables = await service.list_timetable_filter(
            route_id,
            start_stop_id,
            weekdays,
            start.replace(tzinfo=KST) if start is not None else None,
            end.replace(tzinfo=KST) if end is not None else None,
        )
    mapping_func: Callable[
        [BusTimetable],
        dict[str, int | str | datetime.datetime],
    ] = lambda x: {
        "routeID": x.route_id,
        "start": x.start_stop_id,
        "weekdays": x.weekday,
        "departureTime": timestamp_tz_to_datetime(x.departure_time),
    }
    return {"data": map(mapping_func, timetables)}


@router.get(
    "/timetable/{route_id}/{start_stop_id}/{weekday}/{departure_time}",
    response_model=BusTimetableDetailResponse,
)
async def get_bus_timetable_detail(
    weekday: str,
    start_stop_id: int,
    departure_time: datetime.time,
    route_id: int = Depends(get_valid_route),
    _: str = Depends(parse_jwt_user_data),
):
    if await service.get_stop(start_stop_id) is None:
        raise StopNotFound()
    timetable = await service.get_timetable(
        route_id,
        start_stop_id,
        weekday,
        departure_time.replace(tzinfo=KST),
    )
    if timetable is None:
        raise TimetableNotFound()
    return {
        "routeID": timetable.route_id,
        "start": timetable.start_stop_id,
        "weekdays": timetable.weekday,
        "departureTime": timestamp_tz_to_datetime(timetable.departure_time),
    }


@router.post(
    "/timetable",
    status_code=status.HTTP_201_CREATED,
    response_model=BusTimetableDetailResponse,
)
async def create_bus_timetable(
    new_timetable: CreateBusTimetableRequest = Depends(create_valid_timetable),
    _: str = Depends(parse_jwt_user_data),
):
    timetable = await service.create_timetable(new_timetable)
    if timetable is None:
        raise DetailedHTTPException()
    return {
        "routeID": timetable.route_id,
        "start": timetable.start_stop_id,
        "weekdays": timetable.weekday,
        "departureTime": timestamp_tz_to_datetime(timetable.departure_time),
    }


@router.delete(
    "/timetable/{route_id}/{start_stop_id}/{weekday}/{departure_time}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_bus_timetable(
    weekday: str,
    start_stop_id: int,
    departure_time: datetime.time,
    route_id: int = Depends(get_valid_route),
    _: str = Depends(parse_jwt_user_data),
):
    if await service.get_stop(start_stop_id) is None:
        raise StopNotFound()
    elif (
        await service.get_timetable(
            route_id,
            start_stop_id,
            weekday,
            departure_time.replace(tzinfo=KST),
        )
        is None
    ):
        raise TimetableNotFound()
    await service.delete_timetable(
        route_id,
        start_stop_id,
        weekday,
        departure_time.replace(tzinfo=KST),
    )
    return None


@router.get("/realtime", response_model=BusRealtimeListResponse)
async def get_bus_realtime_list(
    stop_id: int | None = None,
    route_id: int | None = None,
    _: str = Depends(parse_jwt_user_data),
):
    if stop_id is None and route_id is None:
        realtime_list = await service.list_realtime()
    else:
        realtime_list = await service.list_realtime_filter(stop_id, route_id)
    mapping_func: Callable[
        [BusRealtime],
        dict[str, int | str | datetime.datetime | datetime.timedelta],
    ] = lambda x: {
        "stopID": x.stop_id,
        "routeID": x.route_id,
        "sequence": x.sequence,
        "stop": x.stops,
        "seat": x.seats,
        "time": x.time,
        "lowFloor": x.low_floor,
        "updatedAt": datetime_to_str(x.updated_at),
    }
    return {"data": map(mapping_func, realtime_list)}
