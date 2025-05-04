import datetime
from typing import Callable

import holidays
import pytz
import strawberry
from pytz import timezone
from sqlalchemy import select
from sqlalchemy.orm import selectinload, load_only, joinedload

from database import fetch_all
from model.bus import BusStop, BusRouteStop, BusTimetable, BusRealtime, BusRoute, BusDepartureLog
from utils import KST


kr_holidays = holidays.country_holidays("KR")


@strawberry.type
class BusStopItem:
    id_: int = strawberry.field(description="Stop ID", name="id")
    name: str = strawberry.field(description="Stop name")
    district_code: int = strawberry.field(
        description="District code", name="districtCode",
    )
    region_name: str = strawberry.field(description="Region name", name="region")
    mobile_number: str = strawberry.field(
        description="Mobile number", name="mobileNumber",
    )
    latitude: float = strawberry.field(description="Latitude")
    longitude: float = strawberry.field(description="Longitude")


@strawberry.type
class BusTimetableQuery:
    weekdays: str = strawberry.field(description="Is weekdays", name="weekdays")
    departure_time: str = strawberry.field(description="Departure time", name="time")
    departure_hour: int = strawberry.field(description="Departure hour")
    departure_minute: int = strawberry.field(description="Departure minute")


@strawberry.type
class BusRealtimeQuery:
    sequence: int = strawberry.field(description="Sequence")
    stop: int = strawberry.field(description="Stop")
    time: float = strawberry.field(description="Time")
    seat: int = strawberry.field(description="Seat")
    low_floor: bool = strawberry.field(description="Low floor", name="lowFloor")
    updated_at: datetime.datetime = strawberry.field(
        description="Updated at", name="updatedAt",
    )


@strawberry.type
class BusRouteCompanyQuery:
    id_: int = strawberry.field(description="Company ID", name="id")
    name: str = strawberry.field(description="Company name")
    telephone: str = strawberry.field(description="Company telephone")


@strawberry.type
class BusRouteTypeQuery:
    code: str = strawberry.field(description="Type code", name="code")
    name: str = strawberry.field(description="Type name")


@strawberry.type
class BusRunningTimeQuery:
    first: str = strawberry.field(description="First time", name="first")
    last: str = strawberry.field(description="Last time", name="last")


@strawberry.type
class BusRunningListQuery:
    up: BusRunningTimeQuery = strawberry.field(description="Up")
    down: BusRunningTimeQuery = strawberry.field(description="Down")


@strawberry.type
class BusRouteQuery:
    id_: int = strawberry.field(description="Route ID", name="id")
    name: str = strawberry.field(description="Route name")
    type_: BusRouteTypeQuery = strawberry.field(description="Type", name="type")
    company: BusRouteCompanyQuery = strawberry.field(description="Company")
    district_code: int = strawberry.field(
        description="District code", name="districtCode",
    )
    running_time: BusRunningListQuery = strawberry.field(
        description="Running time", name="runningTime",
    )
    start_stop: BusStopItem = strawberry.field(description="Start stop", name="start")
    end_stop: BusStopItem = strawberry.field(description="End stop", name="end")


@strawberry.type
class BusDepartureLogQuery:
    departure_date: datetime.date = strawberry.field(description="Departure date")
    departure_time: datetime.time = strawberry.field(description="Departure time")
    departure_hour: int = strawberry.field(description="Departure hour")
    departure_minute: int = strawberry.field(description="Departure minute")
    vehicle_id: str = strawberry.field(description="Vehicle ID", name="vehicleId")


@strawberry.type
class BusStopRouteQuery:
    sequence: int = strawberry.field(description="Sequence")
    info: BusRouteQuery = strawberry.field(description="Info")
    minute_from_start: int = strawberry.field(
        description="Minute from start stop", name="minuteFromStart",
    )
    timetable: list[BusTimetableQuery] = strawberry.field(description="Timetable")
    realtime: list[BusRealtimeQuery] = strawberry.field(description="Realtime")
    log: list[BusDepartureLogQuery] = strawberry.field(description="Log")


@strawberry.type
class StopQuery(BusStopItem):
    routes: list[BusStopRouteQuery] = strawberry.field(description="Routes")


async def resolve_bus(
    id_: list[int] | None = None,
    name: str | None = None,
    route_id: int | None = None,
    routes: list[int] | None = None,
    weekdays: list[str] | None = None,
    log_date: list[datetime.date] | None = None,
    start: datetime.time | None = None,
    start_str: str | None = None,
    end: datetime.time | None = None,
    end_str: str | None = None,
) -> list[StopQuery]:
    stop_conditions = []
    if id_:
        stop_conditions.append(BusStop.id_.in_(id_))
    if name:
        stop_conditions.append(BusStop.name.like(f"%{name}%"))

    stop_query = (
        select(BusStop)
        .options(
            selectinload(BusStop.routes).options(
                load_only(BusRouteStop.sequence, BusRouteStop.minute_from_start),
                selectinload(BusRouteStop.timetable).options(
                    load_only(BusTimetable.weekday, BusTimetable.departure_time),
                ),
                selectinload(BusRouteStop.realtime).options(
                    load_only(
                        BusRealtime.sequence,
                        BusRealtime.stops,
                        BusRealtime.time,
                        BusRealtime.seats,
                        BusRealtime.low_floor,
                        BusRealtime.updated_at,
                    ),
                ),
                selectinload(BusRouteStop.log).options(
                    load_only(
                        BusDepartureLog.date,
                        BusDepartureLog.time,
                        BusDepartureLog.vehicle_id,
                    ),
                ),
                joinedload(BusRouteStop.route).options(
                    load_only(
                        BusRoute.company_id,
                        BusRoute.company_name,
                        BusRoute.company_telephone,
                        BusRoute.district,
                        BusRoute.up_first_time,
                        BusRoute.up_last_time,
                        BusRoute.down_first_time,
                        BusRoute.down_last_time,
                        BusRoute.id_,
                        BusRoute.name,
                        BusRoute.type_code,
                        BusRoute.type_name,
                    ),
                    joinedload(BusRoute.start_stop).options(
                        load_only(
                            BusStop.id_,
                            BusStop.name,
                            BusStop.district,
                            BusStop.region,
                            BusStop.mobile_no,
                            BusStop.latitude,
                            BusStop.longitude,
                        ),
                    ),
                    joinedload(BusRoute.end_stop).options(
                        load_only(
                            BusStop.id_,
                            BusStop.name,
                            BusStop.district,
                            BusStop.region,
                            BusStop.mobile_no,
                            BusStop.latitude,
                            BusStop.longitude,
                        ),
                    ),
                ),
            ),
        )
        .filter(*stop_conditions)
    )
    stops = await fetch_all(stop_query)
    result: list[StopQuery] = []
    now = datetime.datetime.now(tz=pytz.timezone("Asia/Seoul"))
    if weekdays is None:
        if now.isoformat() in kr_holidays or now.weekday() == 6:
            weekdays = ["sunday"]
        elif now.weekday() == 5:
            weekdays = ["saturday"]
        else:
            weekdays = ["weekdays"]
    if isinstance(start_str, str):
        start_value = datetime.datetime.strptime(start_str, "%H:%M:%S").time().replace(tzinfo=KST)
    elif isinstance(start, datetime.time):
        start_value = start.replace(tzinfo=KST)
    else:
        start_value = None
    if isinstance(end_str, str):
        end_value = datetime.datetime.strptime(end_str, "%H:%M:%S").time().replace(tzinfo=KST)
    elif isinstance(end, datetime.time):
        end_value = end.replace(tzinfo=KST)
    else:
        end_value = None
    timetable_filter: Callable[[BusTimetable], bool] = lambda x: (
        x.weekday in weekdays
        and (
            start_value is None
            or (
                x.departure_time.replace(tzinfo=KST) >= start_value or
                x.departure_time.replace(tzinfo=KST) < datetime.time(4, 0, 0).replace(tzinfo=KST)
            )
            if start_value is not None
            else True
        )
        and (
            end_value is None
            or (x.departure_time.replace(tzinfo=KST) <= end_value.replace(tzinfo=KST))
            if end_value is not None
            else True
        )
    )
    realtime_filter: Callable[[BusRealtime], bool] = lambda x: (
        x.updated_at.astimezone(timezone("Asia/Seoul")) >= now - x.time
    )
    for stop in stops:
        result.append(
            StopQuery(
                id_=stop.id_,
                name=stop.name,
                district_code=stop.district,
                region_name=stop.region,
                mobile_number=stop.mobile_no,
                latitude=stop.latitude,
                longitude=stop.longitude,
                routes=[
                    BusStopRouteQuery(
                        sequence=route.sequence,
                        minute_from_start=route.minute_from_start,
                        info=BusRouteQuery(
                            id_=route.route.id_,
                            name=route.route.name,
                            type_=BusRouteTypeQuery(
                                code=route.route.type_code,
                                name=route.route.type_name,
                            ),
                            company=BusRouteCompanyQuery(
                                id_=route.route.company_id,
                                name=route.route.company_name,
                                telephone=route.route.company_telephone,
                            ),
                            district_code=route.route.district,
                            running_time=BusRunningListQuery(
                                up=BusRunningTimeQuery(
                                    first=route.route.up_first_time.strftime(
                                        "%H:%M:%S",
                                    ),
                                    last=route.route.up_last_time.strftime("%H:%M:%S"),
                                ),
                                down=BusRunningTimeQuery(
                                    first=route.route.down_first_time.strftime(
                                        "%H:%M:%S",
                                    ),
                                    last=route.route.down_last_time.strftime(
                                        "%H:%M:%S",
                                    ),
                                ),
                            ),
                            start_stop=BusStopItem(
                                id_=route.route.start_stop.id_,
                                name=route.route.start_stop.name,
                                district_code=route.route.start_stop.district,
                                region_name=route.route.start_stop.region,
                                mobile_number=route.route.start_stop.mobile_no,
                                latitude=route.route.start_stop.latitude,
                                longitude=route.route.start_stop.longitude,
                            ),
                            end_stop=BusStopItem(
                                id_=route.route.end_stop.id_,
                                name=route.route.end_stop.name,
                                district_code=route.route.end_stop.district,
                                region_name=route.route.end_stop.region,
                                mobile_number=route.route.end_stop.mobile_no,
                                latitude=route.route.end_stop.latitude,
                                longitude=route.route.end_stop.longitude,
                            ),
                        ),
                        timetable=[
                            BusTimetableQuery(
                                weekdays=timetable.weekday,
                                departure_time=convert_time_after_midnight(
                                    timetable.departure_time,
                                ),
                                departure_hour=(
                                    timetable.departure_time.hour
                                    if timetable.departure_time.hour < 4 else timetable.departure_time.hour
                                ),
                                departure_minute=timetable.departure_time.minute,
                            )
                            for timetable in sorted(
                                list(filter(timetable_filter, route.timetable)),
                                key=lambda x: convert_time_after_midnight(x.departure_time),
                            )
                        ],
                        realtime=[
                            BusRealtimeQuery(
                                sequence=realtime.sequence,
                                stop=realtime.stops,
                                time=calculate_remaining_time(
                                    realtime.updated_at, realtime.time,
                                ),
                                seat=realtime.seats,
                                low_floor=realtime.low_floor,
                                updated_at=realtime.updated_at.astimezone(
                                    timezone("Asia/Seoul"),
                                ),
                            )
                            for realtime in sorted(
                                list(filter(realtime_filter, route.realtime)),
                                key=lambda x: x.sequence,
                            )
                        ],
                        log=[
                            BusDepartureLogQuery(
                                departure_date=log.date,
                                departure_time=log.time,
                                departure_hour=log.time.hour,
                                departure_minute=log.time.minute,
                                vehicle_id=log.vehicle_id,
                            )
                            for log in sorted(
                                list(
                                    filter(
                                        lambda x: log_date is None or x.date in log_date,
                                        route.log,
                                    ),
                                ), key=lambda x: x.date,
                            )
                        ],
                    )
                    for route in sorted(
                        list(
                            filter(
                                lambda x: (
                                    route_id is not None and x.route.id_ == route_id
                                ) or (
                                    routes is not None and x.route.id_ in routes
                                ) or (
                                    route_id is None and routes is None
                                ),
                                stop.routes,
                            ),
                        ),
                        key=lambda x: x.sequence,
                    )
                ],
            ),
        )
    return result


def calculate_remaining_time(
    updated_at: datetime.datetime,
    time: datetime.timedelta,
) -> float:
    now = datetime.datetime.now(tz=KST)
    remaining_secs = (updated_at + time - now).total_seconds()
    return round(remaining_secs / 60, 1)


def convert_time_after_midnight(
    time: datetime.time,
) -> str:
    if time.replace(tzinfo=KST) < datetime.time(4, 0, 0).replace(tzinfo=KST):
        return f'{24 + time.hour}:{time.strftime("%M:%S")}'
    return time.strftime("%H:%M:%S")
