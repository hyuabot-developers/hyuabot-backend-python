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
from user.jwt import parse_jwt_user_data

router = APIRouter()


@router.get("/route", response_model=CommuteShuttleRouteListResponse)
async def get_route_list(
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.list_route()
    return {
        "data": map(
            lambda x: {
                "route": x["route_name"],
                "korean": x["route_description_korean"],
                "english": x["route_description_english"],
            },
            data,
        ),
    }


@router.get("/route/{route_name}", response_model=CommuteShuttleRouteDetailResponse)
async def get_route(
    route_name: str,
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.get_route(route_name)
    if data is None:
        raise RouteNotFound()
    return {
        "route": data["route_name"],
        "korean": data["route_description_korean"],
        "english": data["route_description_english"],
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
        "route": data["route_name"],
        "korean": data["route_description_korean"],
        "english": data["route_description_english"],
    }


@router.patch(
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
        "route": data["route_name"],
        "korean": data["route_description_korean"],
        "english": data["route_description_english"],
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
    return {
        "data": map(
            lambda x: {
                "name": x["stop_name"],
                "description": x["description"],
                "latitude": x["latitude"],
                "longitude": x["longitude"],
            },
            data,
        ),
    }


@router.get("/stop/{stop_id}", response_model=CommuteShuttleStopDetailResponse)
async def get_stop(
    stop_id: str,
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.get_stop(stop_id)
    if data is None:
        raise StopNotFound()
    return {
        "name": data["stop_name"],
        "description": data["description"],
        "latitude": data["latitude"],
        "longitude": data["longitude"],
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
        "name": data["stop_name"],
        "description": data["description"],
        "latitude": data["latitude"],
        "longitude": data["longitude"],
    }


@router.patch(
    "/stop/{stop_id}",
    response_model=CommuteShuttleStopDetailResponse,
)
async def update_stop(
    new_stop: UpdateCommuteShuttleStopRequest,
    stop_id: str = Depends(get_valid_stop),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.update_stop(stop_id, new_stop)
    if data is None:
        raise DetailedHTTPException()
    return {
        "name": data["stop_name"],
        "description": data["description"],
        "latitude": data["latitude"],
        "longitude": data["longitude"],
    }


@router.delete("/stop/{stop_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_stop(
    stop_id: str = Depends(get_valid_stop),
    _: str = Depends(parse_jwt_user_data),
):
    await service.delete_stop(stop_id)


@router.get("/timetable", response_model=CommuteShuttleTimetableListResponse)
async def get_timetable_list(
    route_name: str | None = None,
    _: str = Depends(parse_jwt_user_data),
):
    if route_name is None:
        data = await service.list_timetable()
    else:
        data = await service.list_timetable_filter(route_name)
    return {
        "data": map(
            lambda x: {
                "route": x["route_name"],
                "stop": x["stop_name"],
                "sequence": x["stop_order"],
                "time": x["departure_time"],
            },
            data,
        ),
    }


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
        "route": data["route_name"],
        "stop": data["stop_name"],
        "sequence": data["stop_order"],
        "time": data["departure_time"],
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
        "route": data["route_name"],
        "stop": data["stop_name"],
        "sequence": data["stop_order"],
        "time": data["departure_time"],
    }


@router.patch(
    "/timetable/{route_name}/{stop_name}",
    response_model=CommuteShuttleTimetableDetailResponse,
)
async def update_timetable(
    new_timetable: UpdateCommuteShuttleTimetableRequest,
    route_name: str = Depends(get_valid_route),
    stop_name: str = Depends(get_valid_stop),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.update_timetable(route_name, stop_name, new_timetable)
    if data is None:
        raise DetailedHTTPException()
    return {
        "route": data["route_name"],
        "stop": data["stop_name"],
        "sequence": data["stop_order"],
        "time": data["departure_time"],
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
