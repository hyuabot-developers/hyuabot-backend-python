import datetime
from typing import Callable, Any

from fastapi import APIRouter, Depends
from starlette import status

from exceptions import DetailedHTTPException
from model.shuttle import (
    ShuttlePeriod,
    ShuttleRoute,
    ShuttleStop,
    ShuttleRouteStop,
    ShuttleTimetable,
    ShuttleTimetableView,
    ShuttleHoliday,
)
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
from utils import timestamp_tz_to_datetime

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
    mapping_func: Callable[[ShuttleHoliday], dict[str, Any]] = lambda x: {
        "date": x.date,
        "type": x.type_,
        "calendar": x.calendar,
    }
    return {"data": map(mapping_func, data)}


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
        "date": data.date,
        "type": data.type_,
        "calendar": data.calendar,
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
        "date": data.date,
        "type": data.type_,
        "calendar": data.calendar,
    }


@router.delete("/holiday/{calendar}/{date}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_holiday(
    calendar: str,
    date: datetime.date,
    _: str = Depends(parse_jwt_user_data),
):
    if await service.get_holiday(calendar, date) is None:
        raise HolidayNotFound()
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
    mapping_func: Callable[[ShuttlePeriod], dict[str, Any]] = lambda x: {
        "type": x.type_id,
        "start": x.start,
        "end": x.end,
    }
    return {"data": map(mapping_func, data)}


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
        "type": data.type_id,
        "start": data.start,
        "end": data.end,
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
        "type": data.type_id,
        "start": data.start,
        "end": data.end,
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
    if (
        await service.get_period(
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
        is None
    ):
        raise PeriodNotFound()
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
    mapping_func: Callable[[ShuttleRoute], dict[str, Any]] = lambda x: {
        "name": x.name,
        "tag": x.tag,
        "korean": x.korean,
        "english": x.english,
        "start": x.start_stop_id,
        "end": x.end_stop_id,
    }
    return {"data": map(mapping_func, data)}


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
        "name": data.name,
        "tag": data.tag,
        "korean": data.korean,
        "english": data.english,
        "start": data.start_stop_id,
        "end": data.end_stop_id,
    }


@router.get("/route/{route_name}", response_model=ShuttleRouteDetailResponse)
async def get_route(
    route_name: str,
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.get_route(route_name)
    if data is None:
        raise RouteNotFound()
    return {
        "name": data.name,
        "tag": data.tag,
        "korean": data.korean,
        "english": data.english,
        "start": data.start_stop_id,
        "end": data.end_stop_id,
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
        "name": data.name,
        "tag": data.tag,
        "korean": data.korean,
        "english": data.english,
        "start": data.start_stop_id,
        "end": data.end_stop_id,
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
    mapping_func: Callable[[ShuttleStop], dict[str, Any]] = lambda x: {
        "name": x.name,
        "latitude": x.latitude,
        "longitude": x.longitude,
    }
    return {"data": map(mapping_func, data)}


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
        "name": data.name,
        "latitude": data.latitude,
        "longitude": data.longitude,
    }


@router.get("/stop/{stop_name}", response_model=ShuttleStopItemResponse)
async def get_stop(
    stop_name: str,
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.get_stop(stop_name)
    if data is None:
        raise StopNotFound()
    return {
        "name": data.name,
        "latitude": data.latitude,
        "longitude": data.longitude,
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
        "name": data.name,
        "latitude": data.latitude,
        "longitude": data.longitude,
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
    mapping_func: Callable[[ShuttleRouteStop], dict[str, Any]] = lambda x: {
        "route": x.route_name,
        "stop": x.stop_name,
        "sequence": x.sequence,
        "cumulativeTime": x.cumulative_time.total_seconds(),
    }
    return {"data": map(mapping_func, data)}


@router.post(
    "/route/{route_name}/stop",
    status_code=status.HTTP_201_CREATED,
    response_model=ShuttleRouteStopItemResponse,
)
async def create_route_stop(
    new_route_stop: CreateShuttleRouteStopRequest,
    route_name: str = Depends(get_valid_route),
    _: str = Depends(parse_jwt_user_data),
):
    new_route_stop = await create_valid_route_stop(route_name, new_route_stop)
    data = await service.create_route_stop(route_name, new_route_stop)
    if data is None:
        raise DetailedHTTPException()
    return {
        "route": data.route_name,
        "stop": data.stop_name,
        "sequence": data.sequence,
        "cumulativeTime": data.cumulative_time.total_seconds(),
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
        "route": data.route_name,
        "stop": data.stop_name,
        "sequence": data.sequence,
        "cumulativeTime": data.cumulative_time.total_seconds(),
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
    data = await service.get_route_stop(route_name, stop_name)
    if data is None:
        raise RouteStopNotFound()
    data = await service.update_route_stop(route_name, stop_name, new_route_stop)
    if data is None:
        raise DetailedHTTPException()
    return {
        "route": data.route_name,
        "stop": data.stop_name,
        "sequence": data.sequence,
        "cumulativeTime": data.cumulative_time.total_seconds(),
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
    if await service.get_route_stop(route_name, stop_name) is None:
        raise RouteStopNotFound()
    await service.delete_route_stop(route_name, stop_name)


@router.get("/timetable", response_model=ShuttleTimetableListResponse)
async def get_timetable_list(
    _: str = Depends(parse_jwt_user_data),
    route: str | None = None,
    weekdays: bool | None = None,
    start: datetime.time | None = None,
    end: datetime.time | None = None,
):
    if any([route, weekdays is not None, start, end]):
        data = await service.list_timetable_filter(
            route=route,
            weekdays=weekdays,
            start_time=start,
            end_time=end,
        )
    else:
        data = await service.list_timetable()
    mapping_func: Callable[[ShuttleTimetable], dict[str, Any]] = lambda x: {
        "sequence": x.id_,
        "period": x.period,
        "weekdays": x.is_weekdays,
        "route": x.route_name,
        "time": timestamp_tz_to_datetime(x.departure_time),
    }
    return {"data": map(mapping_func, data)}


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
        "sequence": data.id_,
        "period": data.period,
        "weekdays": data.is_weekdays,
        "route": data.route_name,
        "time": timestamp_tz_to_datetime(data.departure_time),
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
        "sequence": data.id_,
        "period": data.period,
        "weekdays": data.is_weekdays,
        "route": data.route_name,
        "time": timestamp_tz_to_datetime(data.departure_time),
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
        "sequence": data.id_,
        "period": data.period,
        "weekdays": data.is_weekdays,
        "route": data.route_name,
        "time": timestamp_tz_to_datetime(data.departure_time),
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
    mapping_func: Callable[[ShuttleTimetableView], dict[str, Any]] = lambda x: {
        "sequence": x.id_,
        "period": x.period,
        "weekdays": x.is_weekdays,
        "route": x.route_name,
        "stop": x.stop_name,
        "time": timestamp_tz_to_datetime(x.departure_time),
    }
    return {"data": map(mapping_func, data)}
