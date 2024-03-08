import datetime
from typing import Callable

import strawberry
from pytz import timezone
from sqlalchemy import select
from sqlalchemy.orm import selectinload, load_only, joinedload

from database import fetch_all
from model.subway import SubwayRouteStation, SubwayTimetable, SubwayRealtime
from utils import KST


@strawberry.type
class TimetableStation:
    id_: str = strawberry.field(description="Station ID", name="id")
    name: str = strawberry.field(description="Station name")


@strawberry.type
class TimetableQuery:
    is_weekdays: bool = strawberry.field(description="Is weekdays", name="weekdays")
    departure_time: str = strawberry.field(description="Departure time", name="time")
    start_station: TimetableStation = strawberry.field(
        description="Start station",
        name="start",
    )
    terminal_station: TimetableStation = strawberry.field(
        description="Terminal station",
        name="terminal",
    )


@strawberry.type
class TimetableListQuery:
    up: list[TimetableQuery] = strawberry.field(description="Up")
    down: list[TimetableQuery] = strawberry.field(description="Down")


@strawberry.type
class RealtimeQuery:
    sequence: int = strawberry.field(description="Sequence")
    location: str = strawberry.field(description="Location")
    stop: int = strawberry.field(description="Stop")
    time: float = strawberry.field(description="Time")
    train_no: str = strawberry.field(description="Train number", name="trainNo")
    is_express: bool = strawberry.field(description="Is express", name="express")
    is_last: bool = strawberry.field(description="Is last", name="last")
    status: int = strawberry.field(description="Status")
    terminal_station: TimetableStation = strawberry.field(
        description="Terminal station",
        name="terminal",
    )
    updated_at: datetime.datetime = strawberry.field(
        description="Updated at",
        name="updatedAt",
    )


@strawberry.type
class RealtimeListQuery:
    up: list[RealtimeQuery] = strawberry.field(description="Up")
    down: list[RealtimeQuery] = strawberry.field(description="Down")


@strawberry.type
class StationQuery:
    id_: str = strawberry.field(description="Station ID", name="id")
    name: str = strawberry.field(description="Station name")
    sequence: int = strawberry.field(description="Station sequence")
    route_id: str = strawberry.field(description="Route ID", name="routeID")
    timetable: TimetableListQuery = strawberry.field(description="Timetable")
    realtime: RealtimeListQuery = strawberry.field(description="Realtime")


async def resolve_subway(
    id_: list[str] | None = None,
    name: str | None = None,
    weekdays: bool | None = None,
    start: datetime.time | None = None,
    end: datetime.time | None = None,
) -> list[StationQuery]:
    station_conditions = []
    if id_:
        station_conditions.append(SubwayRouteStation.id_.in_(id_))
    if name:
        station_conditions.append(SubwayRouteStation.name.like(f"%{name}%"))

    station_query = (
        select(SubwayRouteStation)
        .filter(*station_conditions)
        .order_by(SubwayRouteStation.id_)
        .options(
            selectinload(SubwayRouteStation.timetable).options(
                load_only(
                    SubwayTimetable.heading,
                    SubwayTimetable.is_weekdays,
                    SubwayTimetable.departure_time,
                ),
                joinedload(SubwayTimetable.start_station).options(
                    load_only(SubwayRouteStation.id_, SubwayRouteStation.name),
                ),
                joinedload(SubwayTimetable.terminal_station).options(
                    load_only(SubwayRouteStation.id_, SubwayRouteStation.name),
                ),
            ),
            selectinload(SubwayRouteStation.realtime).options(
                load_only(
                    SubwayRealtime.heading,
                    SubwayRealtime.sequence,
                    SubwayRealtime.location,
                    SubwayRealtime.stop,
                    SubwayRealtime.time,
                    SubwayRealtime.train_number,
                    SubwayRealtime.is_express,
                    SubwayRealtime.is_last,
                    SubwayRealtime.status,
                    SubwayRealtime.updated_at,
                ),
                joinedload(SubwayRealtime.terminal_station).options(
                    load_only(SubwayRouteStation.id_, SubwayRouteStation.name),
                ),
            ),
            load_only(
                SubwayRouteStation.id_,
                SubwayRouteStation.route_id,
                SubwayRouteStation.name,
                SubwayRouteStation.sequence,
            ),
        )
    )
    stations = await fetch_all(station_query)
    result: list[StationQuery] = []
    now = datetime.datetime.now(tz=KST)
    timetable_filter: Callable[[SubwayTimetable], bool] = lambda x: (
        ((x.is_weekdays == "weekdays") == weekdays if weekdays is not None else True)
        and (start is None or x.departure_time >= start if start is not None else True)
        and (end is None or x.departure_time <= end if end is not None else True)
    )
    realtime_filter: Callable[[SubwayRealtime], bool] = lambda x: (
        x.updated_at.astimezone(timezone("Asia/Seoul")) >= now - x.time
    )
    for station in stations:
        timetable = list(filter(timetable_filter, station.timetable))
        realtime = list(filter(realtime_filter, station.realtime))
        up_timetable = list(filter(lambda x: x.heading == "up", timetable))
        down_timetable = list(filter(lambda x: x.heading == "down", timetable))
        up_realtime = list(filter(lambda x: x.heading == "true", realtime))
        down_realtime = list(filter(lambda x: x.heading == "false", realtime))
        result.append(
            StationQuery(
                id_=station.id_,
                name=station.name,
                sequence=station.sequence,
                route_id=station.route_id,
                timetable=TimetableListQuery(
                    up=[
                        TimetableQuery(
                            is_weekdays=timetable.is_weekdays == "weekdays",
                            departure_time=timetable.departure_time.strftime(
                                "%H:%M:%S",
                            ),
                            start_station=TimetableStation(
                                id_=timetable.start_station.id_,
                                name=timetable.start_station.name,
                            ),
                            terminal_station=TimetableStation(
                                id_=timetable.terminal_station.id_,
                                name=timetable.terminal_station.name,
                            ),
                        )
                        for timetable in sorted(
                            up_timetable, key=lambda x: x.departure_time,
                        )
                    ],
                    down=[
                        TimetableQuery(
                            is_weekdays=timetable.is_weekdays == "weekdays",
                            departure_time=timetable.departure_time.strftime(
                                "%H:%M:%S",
                            ),
                            start_station=TimetableStation(
                                id_=timetable.start_station.id_,
                                name=timetable.start_station.name,
                            ),
                            terminal_station=TimetableStation(
                                id_=timetable.terminal_station.id_,
                                name=timetable.terminal_station.name,
                            ),
                        )
                        for timetable in sorted(
                            down_timetable, key=lambda x: x.departure_time,
                        )
                    ],
                ),
                realtime=RealtimeListQuery(
                    up=[
                        RealtimeQuery(
                            sequence=realtime.sequence,
                            location=realtime.location,
                            stop=realtime.stop,
                            time=calculate_remaining_time(
                                realtime.updated_at, realtime.time,
                            ),
                            train_no=realtime.train_number,
                            is_express=realtime.is_express,
                            is_last=realtime.is_last,
                            status=realtime.status,
                            terminal_station=TimetableStation(
                                id_=realtime.terminal_station.id_,
                                name=realtime.terminal_station.name,
                            ),
                            updated_at=realtime.updated_at.astimezone(
                                timezone("Asia/Seoul"),
                            ),
                        )
                        for realtime in sorted(up_realtime, key=lambda x: x.sequence)
                    ],
                    down=[
                        RealtimeQuery(
                            sequence=realtime.sequence,
                            location=realtime.location,
                            stop=realtime.stop,
                            time=calculate_remaining_time(
                                realtime.updated_at, realtime.time,
                            ),
                            train_no=realtime.train_number,
                            is_express=realtime.is_express,
                            is_last=realtime.is_last,
                            status=realtime.status,
                            terminal_station=TimetableStation(
                                id_=realtime.terminal_station.id_,
                                name=realtime.terminal_station.name,
                            ),
                            updated_at=realtime.updated_at.astimezone(
                                timezone("Asia/Seoul"),
                            ),
                        )
                        for realtime in sorted(down_realtime, key=lambda x: x.sequence)
                    ],
                ),
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
