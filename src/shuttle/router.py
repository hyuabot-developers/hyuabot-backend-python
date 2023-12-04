import datetime

from fastapi import APIRouter, Depends
from starlette import status

from exceptions import DetailedHTTPException
from shuttle import service
from shuttle.dependancies import (
    create_valid_route,
    get_valid_route,
    create_valid_stop,
    get_valid_stop,
    create_valid_timetable,
    create_valid_period,
    create_valid_holiday,
    get_valid_timetable,
    create_valid_route_stop,
)
from shuttle.exceptions import (
    RouteNotFound,
    StopNotFound,
    TimetableNotFound,
    HolidayNotFound,
    PeriodNotFound,
    RouteStopNotFound,
)
from shuttle.schemas import (
    ShuttleRouteListResponse,
    ShuttleRouteDetailResponse,
    CreateShuttleRouteRequest,
    UpdateShuttleRouteRequest,
    ShuttleStopListResponse,
    ShuttleStopItemResponse,
    CreateShuttleStopRequest,
    UpdateShuttleStopRequest,
    ShuttleTimetableListResponse,
    ShuttleTimetableItemResponse,
    CreateShuttleTimetableRequest,
    UpdateShuttleTimetableRequest,
    ShuttleTimetableViewResponse,
    ShuttlePeriodListResponse,
    ShuttlePeriodItemResponse,
    CreateShuttlePeriodRequest,
    ShuttleHolidayListResponse,
    ShuttleHolidayItemResponse,
    CreateShuttleHolidayRequest,
    ShuttleRouteStopListResponse,
    ShuttleRouteStopItemResponse,
    CreateShuttleRouteStopRequest,
    UpdateShuttleRouteStopRequest,
)
from user.jwt import parse_jwt_user_data
from utils import timedelta_to_str

router = APIRouter()


@router.get("/holiday", response_model=ShuttleHolidayListResponse)
async def get_holiday_list(
    _: str = Depends(parse_jwt_user_data),
    calendar: str | None = None,
    date: datetime.date | None = None,
    start: datetime.date | None = None,
    end: datetime.date | None = None,
):
    if any([calendar, date, start, end]):
        data = await service.list_holiday_filter(
            calendar_type=calendar,
            date=date,
            start_date=start,
            end_date=end,
        )
    else:
        data = await service.list_holiday()
    return {
        "data": map(
            lambda x: {
                "date": x["holiday_date"],
                "type": x["holiday_type"],
                "calendar": x["calendar_type"],
            },
            data,
        ),
    }


@router.post(
    "/holiday",
    status_code=status.HTTP_201_CREATED,
    response_model=ShuttleHolidayItemResponse,
)
async def create_holiday(
    new_holiday: CreateShuttleHolidayRequest = Depends(create_valid_holiday),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.create_holiday(new_holiday)
    if data is None:
        raise DetailedHTTPException()
    return {
        "date": data["holiday_date"],
        "type": data["holiday_type"],
        "calendar": data["calendar_type"],
    }


@router.get("/holiday/{calendar}/{date}", response_model=ShuttleHolidayItemResponse)
async def get_holiday(
    calendar: str,
    date: datetime.date,
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.get_holiday(calendar, date)
    if data is None:
        raise HolidayNotFound()
    return {
        "date": data["holiday_date"],
        "type": data["holiday_type"],
        "calendar": data["calendar_type"],
    }


@router.delete("/holiday/{calendar}/{date}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_holiday(
    calendar: str,
    date: datetime.date,
    _: str = Depends(parse_jwt_user_data),
):
    await service.delete_holiday(calendar, date)


@router.get("/period", response_model=ShuttlePeriodListResponse)
async def get_period_list(
    _: str = Depends(parse_jwt_user_data),
    period: str | None = None,
    date: datetime.date | None = None,
):
    if any([period, date]):
        data = await service.list_period_filter(period_type=period, date=date)
    else:
        data = await service.list_period()
    return {
        "data": map(
            lambda x: {
                "type": x["period_type"],
                "start": x["period_start"],
                "end": x["period_end"],
            },
            data,
        ),
    }


@router.post(
    "/period",
    status_code=status.HTTP_201_CREATED,
    response_model=ShuttlePeriodItemResponse,
)
async def create_period(
    new_period: CreateShuttlePeriodRequest = Depends(create_valid_period),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.create_period(new_period)
    if data is None:
        raise DetailedHTTPException()
    return {
        "type": data["period_type"],
        "start": data["period_start"],
        "end": data["period_end"],
    }


@router.get(
    "/period/{period_type}/{start}/{end}",
    response_model=ShuttlePeriodItemResponse,
)
async def get_period(
    period_type: str,
    start: datetime.date,
    end: datetime.date,
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.get_period(
        period_type,
        datetime.datetime.strptime(
            f"{start}T00:00:00+09:00",
            "%Y-%m-%dT%H:%M:%S%z",
        ),
        datetime.datetime.strptime(
            f"{end}T23:59:59+09:00",
            "%Y-%m-%dT%H:%M:%S%z",
        ),
    )
    if data is None:
        raise PeriodNotFound()
    return {
        "type": data["period_type"],
        "start": data["period_start"],
        "end": data["period_end"],
    }


@router.delete(
    "/period/{period_type}/{start}/{end}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_period(
    period_type: str,
    start: datetime.date,
    end: datetime.date,
    _: str = Depends(parse_jwt_user_data),
):
    await service.delete_period(period_type, start, end)


@router.get("/route", response_model=ShuttleRouteListResponse)
async def get_route_list(
    _: str = Depends(parse_jwt_user_data),
    name: str | None = None,
    tag: str | None = None,
):
    if name is not None or tag is not None:
        data = await service.list_route_filter(name=name, tag=tag)
    else:
        data = await service.list_route()
    return {
        "data": map(
            lambda x: {
                "name": x["route_name"],
                "tag": x["route_tag"],
                "korean": x["route_description_korean"],
                "english": x["route_description_english"],
            },
            data,
        ),
    }


@router.post(
    "/route",
    status_code=status.HTTP_201_CREATED,
    response_model=ShuttleRouteDetailResponse,
)
async def create_route(
    new_route: CreateShuttleRouteRequest = Depends(create_valid_route),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.create_route(new_route)
    if data is None:
        raise DetailedHTTPException()
    return {
        "name": data["route_name"],
        "tag": data["route_tag"],
        "korean": data["route_description_korean"],
        "english": data["route_description_english"],
        "start": data["start_stop"],
        "end": data["end_stop"],
    }


@router.get("/route/{route_name}", response_model=ShuttleRouteDetailResponse)
async def get_route(
    route_name: str = Depends(get_valid_route),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.get_route(route_name)
    if data is None:
        raise RouteNotFound()
    return {
        "name": data["route_name"],
        "tag": data["route_tag"],
        "korean": data["route_description_korean"],
        "english": data["route_description_english"],
        "start": data["start_stop"],
        "end": data["end_stop"],
    }


@router.patch(
    "/route/{route_name}",
    response_model=ShuttleRouteDetailResponse,
)
async def update_route(
    new_route: UpdateShuttleRouteRequest,
    route_name: str = Depends(get_valid_route),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.update_route(route_name, new_route)
    if data is None:
        raise DetailedHTTPException()
    return {
        "name": data["route_name"],
        "tag": data["route_tag"],
        "korean": data["route_description_korean"],
        "english": data["route_description_english"],
        "start": data["start_stop"],
        "end": data["end_stop"],
    }


@router.delete("/route/{route_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_route(
    route_name: str = Depends(get_valid_route),
    _: str = Depends(parse_jwt_user_data),
):
    await service.delete_route(route_name)


@router.get("/stop", response_model=ShuttleStopListResponse)
async def get_stop_list(
    _: str = Depends(parse_jwt_user_data),
    name: str | None = None,
):
    if name is not None:
        data = await service.list_stop_filter(name=name)
    else:
        data = await service.list_stop()
    return {
        "data": map(
            lambda x: {
                "name": x["stop_name"],
                "latitude": x["latitude"],
                "longitude": x["longitude"],
            },
            data,
        ),
    }


@router.post(
    "/stop",
    status_code=status.HTTP_201_CREATED,
    response_model=ShuttleStopItemResponse,
)
async def create_stop(
    new_stop: CreateShuttleStopRequest = Depends(create_valid_stop),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.create_stop(new_stop)
    if data is None:
        raise DetailedHTTPException()
    return {
        "name": data["stop_name"],
        "latitude": data["latitude"],
        "longitude": data["longitude"],
    }


@router.get("/stop/{stop_name}", response_model=ShuttleStopItemResponse)
async def get_stop(
    stop_name: str = Depends(get_valid_stop),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.get_stop(stop_name)
    if data is None:
        raise StopNotFound()
    return {
        "name": data["stop_name"],
        "latitude": data["latitude"],
        "longitude": data["longitude"],
    }


@router.patch(
    "/stop/{stop_name}",
    response_model=ShuttleStopItemResponse,
)
async def update_stop(
    new_stop: UpdateShuttleStopRequest,
    stop_name: str = Depends(get_valid_stop),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.update_stop(stop_name, new_stop)
    if data is None:
        raise DetailedHTTPException()
    return {
        "name": data["stop_name"],
        "latitude": data["latitude"],
        "longitude": data["longitude"],
    }


@router.delete("/stop/{stop_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_stop(
    stop_name: str = Depends(get_valid_stop),
    _: str = Depends(parse_jwt_user_data),
):
    await service.delete_stop(stop_name)


@router.get("/route/{route_name}/stop", response_model=ShuttleRouteStopListResponse)
async def get_route_stop_list(
    route_name: str = Depends(get_valid_route),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.list_route_stop_filter(route_name)
    return {
        "data": map(
            lambda x: {
                "route": x["route_name"],
                "stop": x["stop_name"],
                "sequence": x["stop_order"],
                "cumulativeTime": x["cumulative_time"],
            },
            data,
        ),
    }


@router.post(
    "/route/{route_name}/stop",
    status_code=status.HTTP_201_CREATED,
    response_model=ShuttleRouteStopItemResponse,
)
async def create_route_stop(
    new_route_stop: CreateShuttleRouteStopRequest = Depends(create_valid_route_stop),
    route_name: str = Depends(get_valid_route),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.create_route_stop(route_name, new_route_stop)
    if data is None:
        raise DetailedHTTPException()
    return {
        "route": data["route_name"],
        "stop": data["stop_name"],
        "sequence": data["stop_order"],
        "cumulativeTime": timedelta_to_str(data["cumulative_time"]),
    }


@router.get(
    "/route/{route_name}/stop/{stop_name}",
    response_model=ShuttleRouteStopItemResponse,
)
async def get_route_stop(
    route_name: str = Depends(get_valid_route),
    stop_name: str = Depends(get_valid_stop),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.get_route_stop(route_name, stop_name)
    if data is None:
        raise RouteStopNotFound()
    return {
        "route": data["route_name"],
        "stop": data["stop_name"],
        "sequence": data["stop_order"],
        "cumulativeTime": timedelta_to_str(data["cumulative_time"]),
    }


@router.patch(
    "/route/{route_name}/stop/{stop_name}",
    response_model=ShuttleRouteStopItemResponse,
)
async def update_route_stop(
    new_route_stop: UpdateShuttleRouteStopRequest,
    route_name: str = Depends(get_valid_route),
    stop_name: str = Depends(get_valid_stop),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.update_route_stop(route_name, stop_name, new_route_stop)
    if data is None:
        raise DetailedHTTPException()
    return {
        "route": data["route_name"],
        "stop": data["stop_name"],
        "sequence": data["stop_order"],
        "cumulativeTime": timedelta_to_str(data["cumulative_time"]),
    }


@router.delete(
    "/route/{route_name}/stop/{stop_name}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_route_stop(
    route_name: str = Depends(get_valid_route),
    stop_name: str = Depends(get_valid_stop),
    _: str = Depends(parse_jwt_user_data),
):
    await service.delete_route_stop(route_name, stop_name)


@router.get("/timetable", response_model=ShuttleTimetableListResponse)
async def get_timetable_list(
    _: str = Depends(parse_jwt_user_data),
    route: str | None = None,
    weekdays: bool | None = None,
    start: datetime.time | None = None,
    end: datetime.time | None = None,
):
    if any([route, weekdays, start, end]):
        data = await service.list_timetable_filter(
            route=route,
            weekdays=weekdays,
            start_time=start,
            end_time=end,
        )
    else:
        data = await service.list_timetable()
    return {
        "data": map(
            lambda x: {
                "sequence": x["seq"],
                "period": x["period_type"],
                "weekdays": x["weekday"],
                "route": x["route_name"],
                "time": x["departure_time"],
            },
            data,
        ),
    }


@router.post(
    "/timetable",
    status_code=status.HTTP_201_CREATED,
    response_model=ShuttleTimetableItemResponse,
)
async def create_timetable(
    new_timetable: CreateShuttleTimetableRequest = Depends(create_valid_timetable),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.create_timetable(new_timetable)
    if data is None:
        raise DetailedHTTPException()
    return {
        "sequence": data["seq"],
        "period": data["period_type"],
        "weekdays": data["weekday"],
        "route": data["route_name"],
        "time": data["departure_time"],
    }


@router.get(
    "/timetable/{seq}",
    response_model=ShuttleTimetableItemResponse,
)
async def get_timetable(
    seq: int,
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.get_timetable(seq)
    if data is None:
        raise TimetableNotFound()
    return {
        "sequence": data["seq"],
        "period": data["period_type"],
        "weekdays": data["weekday"],
        "route": data["route_name"],
        "time": data["departure_time"],
    }


@router.patch(
    "/timetable/{seq}",
    response_model=ShuttleTimetableItemResponse,
)
async def update_timetable(
    new_timetable: UpdateShuttleTimetableRequest,
    seq: int = Depends(get_valid_timetable),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.update_timetable(seq, new_timetable)
    if data is None:
        raise DetailedHTTPException()
    return {
        "sequence": data["seq"],
        "period": data["period_type"],
        "weekdays": data["weekday"],
        "route": data["route_name"],
        "time": data["departure_time"],
    }


@router.delete("/timetable/{seq}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_timetable(
    seq: int = Depends(get_valid_timetable),
    _: str = Depends(parse_jwt_user_data),
):
    await service.delete_timetable(seq)


@router.get("/timetable-view", response_model=ShuttleTimetableViewResponse)
async def get_timetable_view(
    _: str = Depends(parse_jwt_user_data),
    route: str | None = None,
    stop: str | None = None,
    weekdays: bool | None = None,
    start: datetime.time | None = None,
    end: datetime.time | None = None,
):
    if any([route, weekdays is not None, stop, start, end]):
        data = await service.list_timetable_view_filter(
            route=route,
            stop=stop,
            weekdays=weekdays,
            start_time=start,
            end_time=end,
        )
    else:
        data = await service.list_timetable_view()
    return {
        "data": map(
            lambda x: {
                "sequence": x["seq"],
                "period": x["period_type"],
                "weekdays": x["weekday"],
                "route": x["route_name"],
                "stop": x["stop_name"],
                "time": x["departure_time"],
            },
            data,
        ),
    }
