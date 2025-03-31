from datetime import time
from typing import Callable

from fastapi import APIRouter, Depends
from starlette import status

from commute_shuttle import service
from commute_shuttle.dependancies import (
    create_valid_route,
    get_valid_route,
    create_valid_stop,
    get_valid_stop,
    create_valid_timetable,
)
from commute_shuttle.exceptions import (
    RouteNotFound,
    StopNotFound,
    TimetableNotFound,
)
from commute_shuttle.schemas import (
    CommuteShuttleRouteListResponse,
    CommuteShuttleRouteDetailResponse,
    CreateCommuteShuttleRouteRequest,
    UpdateCommuteShuttleRouteRequest,
    CommuteShuttleStopListResponse,
    CommuteShuttleStopDetailResponse,
    CreateCommuteShuttleStopRequest,
    UpdateCommuteShuttleStopRequest,
    CommuteShuttleTimetableListResponse,
    CommuteShuttleTimetableDetailResponse,
    CreateCommuteShuttleTimetableRequest,
    UpdateCommuteShuttleTimetableRequest,
)
from exceptions import DetailedHTTPException
from model.commute_shuttle import (
    CommuteShuttleRoute,
    CommuteShuttleStop,
    CommuteShuttleTimetable,
)
from user.jwt import parse_jwt_user_data

router = APIRouter()


@router.get("/route", response_model=CommuteShuttleRouteListResponse)
async def get_route_list(
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.list_route()
    mapping_func: Callable[[CommuteShuttleRoute], dict[str, str]] = lambda x: {
        "name": x.name,
        "korean": x.korean,
        "english": x.english,
    }
    return {"data": map(mapping_func, data)}


@router.get("/route/{route_name}", response_model=CommuteShuttleRouteDetailResponse)
async def get_route(
    route_name: str,
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.get_route(route_name)
    if data is None:
        raise RouteNotFound()
    return {
        "name": data.name,
        "korean": data.korean,
        "english": data.english,
    }


@router.post(
    "/route",
    response_model=CommuteShuttleRouteDetailResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_route(
    new_route: CreateCommuteShuttleRouteRequest = Depends(create_valid_route),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.create_route(new_route)
    if data is None:
        raise DetailedHTTPException()
    return {
        "name": data.name,
        "korean": data.korean,
        "english": data.english,
    }


@router.put(
    "/route/{route_name}",
    response_model=CommuteShuttleRouteDetailResponse,
)
async def update_route(
    new_route: UpdateCommuteShuttleRouteRequest,
    route_name: str = Depends(get_valid_route),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.update_route(route_name, new_route)
    if data is None:
        raise DetailedHTTPException()
    return {
        "name": data.name,
        "korean": data.korean,
        "english": data.english,
    }


@router.delete("/route/{route_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_route(
    route_name: str = Depends(get_valid_route),
    _: str = Depends(parse_jwt_user_data),
):
    await service.delete_route(route_name)


@router.get("/stop", response_model=CommuteShuttleStopListResponse)
async def get_stop_list(
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.list_stop()
    mapping_func: Callable[[CommuteShuttleStop], dict[str, str | float]] = lambda x: {
        "name": x.name,
        "description": x.description,
        "latitude": x.latitude,
        "longitude": x.longitude,
    }
    return {"data": map(mapping_func, data)}


@router.get("/stop/{stop_name}", response_model=CommuteShuttleStopDetailResponse)
async def get_stop(
    stop_name: str,
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.get_stop(stop_name)
    if data is None:
        raise StopNotFound()
    return {
        "name": data.name,
        "description": data.description,
        "latitude": data.latitude,
        "longitude": data.longitude,
    }


@router.post(
    "/stop",
    response_model=CommuteShuttleStopDetailResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_stop(
    new_stop: CreateCommuteShuttleStopRequest = Depends(create_valid_stop),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.create_stop(new_stop)
    if data is None:
        raise DetailedHTTPException()
    return {
        "name": data.name,
        "description": data.description,
        "latitude": data.latitude,
        "longitude": data.longitude,
    }


@router.put(
    "/stop/{stop_name}",
    response_model=CommuteShuttleStopDetailResponse,
)
async def update_stop(
    new_stop: UpdateCommuteShuttleStopRequest,
    stop_name: str = Depends(get_valid_stop),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.update_stop(stop_name, new_stop)
    if data is None:
        raise DetailedHTTPException()
    return {
        "name": data.name,
        "description": data.description,
        "latitude": data.latitude,
        "longitude": data.longitude,
    }


@router.delete("/stop/{stop_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_stop(
    stop_name: str = Depends(get_valid_stop),
    _: str = Depends(parse_jwt_user_data),
):
    await service.delete_stop(stop_name)


@router.get("/timetable", response_model=CommuteShuttleTimetableListResponse)
async def get_timetable_list(
    route: str | None = None,
    _: str = Depends(parse_jwt_user_data),
):
    if route is None:
        data = await service.list_timetable()
    else:
        data = await service.list_timetable_filter(route)
    mapping_func: Callable[
        [CommuteShuttleTimetable],
        dict[str, str | int | time],
    ] = lambda x: {
        "name": x.route_name,
        "stop": x.stop_name,
        "sequence": x.sequence,
        "time": x.time,
    }
    return {"data": map(mapping_func, data)}


@router.get(
    "/timetable/{route_name}/{stop_name}",
    response_model=CommuteShuttleTimetableDetailResponse,
)
async def get_timetable(
    route_name: str = Depends(get_valid_route),
    stop_name: str = Depends(get_valid_stop),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.get_timetable(route_name, stop_name)
    if data is None:
        raise TimetableNotFound()
    return {
        "name": data.route_name,
        "stop": data.stop_name,
        "sequence": data.sequence,
        "time": data.time,
    }


@router.post(
    "/timetable",
    response_model=CommuteShuttleTimetableDetailResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_timetable(
    new_timetable: CreateCommuteShuttleTimetableRequest = Depends(
        create_valid_timetable,
    ),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.create_timetable(new_timetable)
    if data is None:
        raise DetailedHTTPException()
    return {
        "name": data.route_name,
        "stop": data.stop_name,
        "sequence": data.sequence,
        "time": data.time,
    }


@router.put(
    "/timetable/{route_name}/{stop_name}",
    response_model=CommuteShuttleTimetableDetailResponse,
)
async def update_timetable(
    new_timetable: UpdateCommuteShuttleTimetableRequest,
    route_name: str = Depends(get_valid_route),
    stop_name: str = Depends(get_valid_stop),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.get_timetable(route_name, stop_name)
    if data is None:
        raise TimetableNotFound()
    data = await service.update_timetable(route_name, stop_name, new_timetable)
    if data is None:
        raise DetailedHTTPException()
    return {
        "name": data.route_name,
        "stop": data.stop_name,
        "sequence": data.sequence,
        "time": data.time,
    }


@router.delete(
    "/timetable/{route_name}/{stop_name}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_timetable(
    route_name: str = Depends(get_valid_route),
    stop_name: str = Depends(get_valid_stop),
    _: str = Depends(parse_jwt_user_data),
):
    await service.delete_timetable(route_name, stop_name)
