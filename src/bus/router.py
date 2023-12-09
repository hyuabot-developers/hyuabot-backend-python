import datetime

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
from user.jwt import parse_jwt_user_data

router = APIRouter()


@router.get("/route", response_model=BusRouteListResponse)
async def get_bus_route_list(
    name: str | None = None,
    type_: str | None = None,
    company: str | None = None,
    _: str = Depends(parse_jwt_user_data),
):
    if name is None and type_ is None and company is None:
        routes = await service.list_routes()
    else:
        routes = await service.list_routes_filter(name, type_, company)
    return {
        "data": map(
            lambda route: {
                "id": route["route_id"],
                "name": route["route_name"],
                "type": route["route_type_name"],
            },
            routes,
        ),
    }


@router.get("/route/{route_id}", response_model=BusRouteDetailResponse)
async def get_bus_route_detail(
    route_id: int,
    _: str = Depends(parse_jwt_user_data),
):
    if service.get_route(route_id) is None:
        raise RouteNotFound()
    route = await service.get_route(route_id)
    if route is None:
        raise DetailedHTTPException()
    return {
        "id": route["route_id"],
        "name": route["route_name"],
        "type": route["route_type_name"],
        "start": route["start_stop_id"],
        "end": route["end_stop_id"],
        "company": {
            "id": route["company_id"],
            "name": route["company_name"],
            "telephone": route["company_telephone"],
        },
        "up": {
            "first": route["up_first_time"],
            "last": route["up_last_time"],
        },
        "down": {
            "first": route["down_first_time"],
            "last": route["down_last_time"],
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
        "id": route["route_id"],
        "name": route["route_name"],
        "type": route["route_type_name"],
        "start": route["start_stop_id"],
        "end": route["end_stop_id"],
        "company": {
            "id": route["company_id"],
            "name": route["company_name"],
            "telephone": route["company_telephone"],
        },
        "up": {
            "first": route["up_first_time"],
            "last": route["up_last_time"],
        },
        "down": {
            "first": route["down_first_time"],
            "last": route["down_last_time"],
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
        "id": route["route_id"],
        "name": route["route_name"],
        "type": route["route_type_name"],
        "start": route["start_stop_id"],
        "end": route["end_stop_id"],
        "company": {
            "id": route["company_id"],
            "name": route["company_name"],
            "telephone": route["company_telephone"],
        },
        "up": {
            "first": route["up_first_time"],
            "last": route["up_last_time"],
        },
        "down": {
            "first": route["down_first_time"],
            "last": route["down_last_time"],
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
    return {
        "data": map(
            lambda stop: {
                "id": stop["stop_id"],
                "name": stop["stop_name"],
            },
            stops,
        ),
    }


@router.get("/stop/{stop_id}", response_model=BusStopDetailResponse)
async def get_bus_stop_detail(
    stop_id: int,
    _: str = Depends(parse_jwt_user_data),
):
    if service.get_stop(stop_id) is None:
        raise StopNotFound()
    stop = await service.get_stop(stop_id)
    if stop is None:
        raise DetailedHTTPException()
    return {
        "id": stop["stop_id"],
        "name": stop["stop_name"],
        "latitude": stop["latitude"],
        "longitude": stop["longitude"],
        "district": stop["district_code"],
        "mobileNumber": stop["mobile_number"],
        "regionName": stop["region_name"],
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
        "id": stop["stop_id"],
        "name": stop["stop_name"],
        "latitude": stop["latitude"],
        "longitude": stop["longitude"],
        "district": stop["district_code"],
        "mobileNumber": stop["mobile_number"],
        "regionName": stop["region_name"],
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
        "id": stop["stop_id"],
        "name": stop["stop_name"],
        "latitude": stop["latitude"],
        "longitude": stop["longitude"],
        "district": stop["district_code"],
        "mobileNumber": stop["mobile_number"],
        "regionName": stop["region_name"],
    }


@router.delete("/stop/{stop_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bus_stop(
    stop_id: int = Depends(get_valid_stop),
    _: str = Depends(parse_jwt_user_data),
):
    await service.delete_stop(stop_id)
    return None


@router.get("/route/{route_id}/stop", response_model=BusRouteStopListResponse)
async def get_bus_route_stop_list(
    route_id: int = Depends(get_valid_route),
    _: str = Depends(parse_jwt_user_data),
):
    if service.get_route(route_id) is None:
        raise RouteNotFound()
    route_stops = await service.list_route_stops(route_id)
    return {
        "data": map(
            lambda route_stop: {
                "id": route_stop["stop_id"],
                "name": route_stop["stop_name"],
                "sequence": route_stop["stop_sequence"],
                "start": route_stop["start_stop_id"],
            },
            route_stops,
        ),
    }


@router.get(
    "/route/{route_id}/stop/{stop_id}",
    response_model=BusRouteStopDetailResponse,
)
async def get_bus_route_stop_detail(
    route_id: int = Depends(get_valid_route),
    stop_id: int = Depends(get_valid_stop),
    _: str = Depends(parse_jwt_user_data),
):
    if service.get_route_stop(route_id, stop_id) is None:
        raise RouteStopNotFound()
    route_stop = await service.get_route_stop(route_id, stop_id)
    if route_stop is None:
        raise DetailedHTTPException()
    return {
        "id": route_stop["stop_id"],
        "name": route_stop["stop_name"],
        "sequence": route_stop["stop_sequence"],
        "start": route_stop["start_stop_id"],
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
    if service.get_route_stop(route_id, new_route_stop.stop_id) is not None:
        raise DuplicateRouteStop()
    route_stop = await service.create_route_stop(route_id, new_route_stop)
    if route_stop is None:
        raise DetailedHTTPException()
    return {
        "id": route_stop["stop_id"],
        "name": route_stop["stop_name"],
        "sequence": route_stop["stop_sequence"],
        "start": route_stop["start_stop_id"],
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
    if service.get_route_stop(route_id, stop_id) is None:
        raise RouteStopNotFound()
    route_stop = await service.update_route_stop(route_id, stop_id, payload)
    if route_stop is None:
        raise DetailedHTTPException()
    return {
        "id": route_stop["stop_id"],
        "name": route_stop["stop_name"],
        "sequence": route_stop["stop_sequence"],
        "start": route_stop["start_stop_id"],
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
    await service.delete_route_stop(route_id, stop_id)
    return None


@router.get("/timetable", response_model=BusTimetableListResponse)
async def get_bus_timetable_list(
    route_id: int | None = None,
    start_stop_id: int | None = None,
    weekday: str | None = None,
    start: datetime.time | None = None,
    end: datetime.time | None = None,
    _: str = Depends(parse_jwt_user_data),
):
    if (
        route_id is None
        and start_stop_id is None
        and weekday is None
        and start is None
        and end is None
    ):
        timetables = await service.list_timetable()
    else:
        timetables = await service.list_timetable_filter(
            route_id,
            start_stop_id,
            weekday,
            start,
            end,
        )
    return {
        "data": map(
            lambda timetable: {
                "routeID": timetable["route_id"],
                "start": timetable["start_stop_id"],
                "weekdays": timetable["weekday"],
                "departureTime": timetable["departure_time"],
            },
            timetables,
        ),
    }


@router.get(
    "/timetable/{route_id}/{start_stop_id}/{weekday}/{departure_time}",
    response_model=BusTimetableDetailResponse,
)
async def get_bus_timetable_detail(
    weekday: str,
    departure_time: datetime.time,
    route_id: int = Depends(get_valid_route),
    start_stop_id: int = Depends(get_valid_stop),
    _: str = Depends(parse_jwt_user_data),
):
    if service.get_timetable(route_id, start_stop_id, weekday, departure_time) is None:
        raise TimetableNotFound()
    timetable = await service.get_timetable(
        route_id,
        start_stop_id,
        weekday,
        departure_time,
    )
    if timetable is None:
        raise DetailedHTTPException()
    return {
        "routeID": timetable["route_id"],
        "start": timetable["start_stop_id"],
        "weekdays": timetable["weekday"],
        "departureTime": timetable["departure_time"],
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
        "routeID": timetable["route_id"],
        "start": timetable["start_stop_id"],
        "weekdays": timetable["weekday"],
        "departureTime": timetable["departure_time"],
    }


@router.delete(
    "/timetable/{route_id}/{start_stop_id}/{weekday}/{departure_time}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_bus_timetable(
    weekday: str,
    departure_time: datetime.time,
    route_id: int = Depends(get_valid_route),
    start_stop_id: int = Depends(get_valid_stop),
    _: str = Depends(parse_jwt_user_data),
):
    await service.delete_timetable(route_id, start_stop_id, weekday, departure_time)
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
    return {
        "data": map(
            lambda realtime: {
                "stopID": realtime["stop_id"],
                "routeID": realtime["route_id"],
                "sequence": realtime["arrival_sequence"],
                "stop": realtime["remaining_stop_count"],
                "seat": realtime["remaining_seat_count"],
                "time": realtime["remaining_time"],
                "lowFloor": realtime["low_plate"],
                "updatedAt": realtime["last_updated"],
            },
            realtime_list,
        ),
    }
