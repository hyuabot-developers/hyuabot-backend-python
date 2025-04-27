import datetime

import holidays
import pytz
import strawberry
from korean_lunar_calendar import KoreanLunarCalendar
from pytz import timezone
from sqlalchemy import select, and_, true, false, or_, ColumnElement, func
from sqlalchemy.orm import load_only, selectinload, joinedload, aliased

from database import fetch_one, fetch_all
from model.shuttle import (
    ShuttleTimetableView,
    ShuttlePeriod,
    ShuttleHoliday,
    ShuttleStop,
    ShuttleRouteStop,
    ShuttleRoute, ShuttleTimetableGroupedView,
)
from shuttle.exceptions import PeriodNotFound
from utils import KST

lunar_calendar = KoreanLunarCalendar()
kr_holidays = holidays.country_holidays("KR")


@strawberry.type
class ShuttleViaQuery:
    stop: str = strawberry.field(name="stop")
    departure_time: str = strawberry.field(name="time")
    departure_hour: int = strawberry.field(name="hour")
    departure_minute: int = strawberry.field(name="minute")


@strawberry.type
class ShuttleTimetableQuery:
    id_: int = strawberry.field(name="id")
    period: str = strawberry.field(name="period")
    is_weekdays: bool = strawberry.field(name="weekdays")
    route_name: str = strawberry.field(name="route")
    route_tag: str = strawberry.field(name="tag")
    stop_name: str = strawberry.field(name="stop")
    departure_time: str = strawberry.field(name="time")
    departure_hour: int = strawberry.field(name="hour")
    departure_minute: int = strawberry.field(name="minute")
    via: list[ShuttleViaQuery] = strawberry.field(name="via")


@strawberry.type
class ShuttleTimetableGroupedQuery:
    id_: int = strawberry.field(name="id")
    period: str = strawberry.field(name="period")
    is_weekdays: bool = strawberry.field(name="weekdays")
    route_name: str = strawberry.field(name="route")
    route_tag: str = strawberry.field(name="tag")
    stop_name: str = strawberry.field(name="stop")
    destination_group: str = strawberry.field(name="destination")
    departure_time: str = strawberry.field(name="time")
    departure_hour: int = strawberry.field(name="hour")
    departure_minute: int = strawberry.field(name="minute")


@strawberry.type
class ShuttlePeriodQuery:
    start: datetime.datetime = strawberry.field(name="start")
    end: datetime.datetime = strawberry.field(name="end")
    type_: str = strawberry.field(name="type")


@strawberry.type
class ShuttleHolidayQuery:
    date: datetime.date = strawberry.field(name="date")
    calendar: str = strawberry.field(name="calendar")
    type_: str = strawberry.field(name="type")


@strawberry.type
class ShuttleStopRouteQuery:
    name: str = strawberry.field(name="name")
    tag: str = strawberry.field(name="tag")
    start: str = strawberry.field(name="start")
    end: str = strawberry.field(name="end")
    korean: str = strawberry.field(name="korean")
    english: str = strawberry.field(name="english")


@strawberry.type
class ShuttleRouteStopQuery:
    name: str = strawberry.field(name="name")
    sequence: int = strawberry.field(name="sequence")


@strawberry.type
class ShuttleRouteQuery:
    name: str = strawberry.field(name="name")
    tag: str = strawberry.field(name="tag")
    start: str = strawberry.field(name="start")
    end: str = strawberry.field(name="end")
    korean: str = strawberry.field(name="korean")
    english: str = strawberry.field(name="english")
    stops: list[ShuttleRouteStopQuery] = strawberry.field(name="stops")


@strawberry.type
class ShuttleStopQuery:
    name: str = strawberry.field(name="name")
    latitude: float = strawberry.field(name="latitude")
    longitude: float = strawberry.field(name="longitude")
    routes: list[ShuttleStopRouteQuery] = strawberry.field(name="routes")


@strawberry.type
class ShuttleQuery:
    period: list[ShuttlePeriodQuery] = strawberry.field(name="period")
    holiday: list[ShuttleHolidayQuery] = strawberry.field(name="holiday")
    stop: list[ShuttleStopQuery] = strawberry.field(name="stop")
    route: list[ShuttleRouteQuery] = strawberry.field(name="route")
    timetable: list[ShuttleTimetableQuery] = strawberry.field(name="timetable")
    grouped_timetable: list[ShuttleTimetableGroupedQuery] = strawberry.field(name="groupedTimetable")


async def resolve_shuttle(
    timestamp: datetime.datetime | None = datetime.datetime.now().astimezone(
        tz=timezone("Asia/Seoul"),
    ),
    period: list[str] | None = None,
    weekdays: list[bool] | None = None,
    route_name: list[str] | None = None,
    route_tag: list[str] | None = None,
    route_start: list[str] | None = None,
    route_end: list[str] | None = None,
    stop_name: list[str] | None = None,
    start: datetime.time | None = None,
    end: datetime.time | None = None,
    period_current: bool | None = None,
    period_start: datetime.date | None = None,
    period_end: datetime.date | None = None,
    count: int = 3,
    group: str = "destination",
) -> ShuttleQuery:
    return ShuttleQuery(
        period=(
            await resolve_shuttle_period(
                start=period_start,
                end=period_end,
                current=period_current,
            )
        ),
        holiday=(await resolve_shuttle_holiday()),
        stop=(await resolve_shuttle_stop(stop_name=stop_name)),
        route=(
            await resolve_shuttle_route(
                route_name=route_name,
                route_tag=route_tag,
                start_stop=route_start,
                end_stop=route_end,
            )
        ),
        timetable=(
            await resolve_shuttle_timetable(
                timestamp=timestamp,
                period=period,
                weekdays=weekdays,
                route_name=route_name,
                route_tag=route_tag,
                stop_name=stop_name,
                start=start,
                end=end,
            )
        ),
        grouped_timetable=(
            await resolve_shuttle_grouped_timetable(
                timestamp=timestamp,
                count=count,
                group=group,
                period=period,
                weekdays=weekdays,
                route_name=route_name,
                route_tag=route_tag,
                stop_name=stop_name,
                start=start,
                end=end,
            )
        )
    )


async def resolve_shuttle_timetable(
    timestamp: datetime.datetime | None = datetime.datetime.now(tz=pytz.timezone("Asia/Seoul")),
    period: list[str] | None = None,
    weekdays: list[bool] | None = None,
    route_name: list[str] | None = None,
    route_tag: list[str] | None = None,
    stop_name: list[str] | None = None,
    start: datetime.time | None = None,
    end: datetime.time | None = None,
) -> list[ShuttleTimetableQuery]:
    timetable_condition: list[ColumnElement[bool] | ColumnElement[bool]] = []
    if period:
        timetable_condition.append(ShuttleTimetableView.period.in_(period))
    elif timestamp:
        select_period_query = (
            select(ShuttlePeriod)
            .options(load_only(ShuttlePeriod.type_id))
            .where(
                and_(
                    ShuttlePeriod.start <= timestamp,
                    ShuttlePeriod.end >= timestamp,
                ),
            )
            .order_by(ShuttlePeriod.type_id.desc())
        )
        current_period = await fetch_one(select_period_query)
        if current_period is None:
            raise PeriodNotFound()
        timetable_condition.append(
            ShuttleTimetableView.period == current_period.type_id,
        )
    if weekdays == [True]:
        timetable_condition.append(ShuttleTimetableView.is_weekdays.is_(true()))
    elif weekdays == [False]:
        timetable_condition.append(ShuttleTimetableView.is_weekdays.is_(false()))
    elif weekdays is None and timestamp:
        lunar_calendar.setSolarDate(timestamp.year, timestamp.month, timestamp.day)
        lunar_date = lunar_calendar.LunarIsoFormat()
        try:
            formatted_lunar_date = datetime.date.fromisoformat(lunar_date)
            select_holiday_query = (
                select(ShuttleHoliday)
                .options(load_only(ShuttleHoliday.type_))
                .where(
                    or_(
                        and_(
                            ShuttleHoliday.date == timestamp.date(),
                            ShuttleHoliday.calendar == "solar",
                        ),
                        and_(
                            ShuttleHoliday.date == formatted_lunar_date,
                            ShuttleHoliday.calendar == "lunar",
                        ),
                    ),
                )
            )
        except ValueError:
            select_holiday_query = (
                select(ShuttleHoliday)
                .options(load_only(ShuttleHoliday.type_))
                .where(
                    and_(
                        ShuttleHoliday.date == timestamp.date(),
                        ShuttleHoliday.calendar == "solar",
                    ),
                )
            )

        holiday = await fetch_one(select_holiday_query)
        if holiday is not None:
            if holiday.type_ == "weekends":
                timetable_condition.append(
                    ShuttleTimetableView.is_weekdays.is_(false()),
                )
            elif holiday.type_ == "halt":
                return []
        else:
            if timestamp.isoformat() in kr_holidays:
                timetable_condition.append(
                    ShuttleTimetableView.is_weekdays.is_(false()))
            elif timestamp.weekday() >= 5:
                timetable_condition.append(ShuttleTimetableView.is_weekdays.is_(false()))
            else:
                timetable_condition.append(ShuttleTimetableView.is_weekdays.is_(true()))
    if route_name:
        timetable_condition.append(ShuttleTimetableView.route_name.in_(route_name))
    if route_tag:
        timetable_condition.append(ShuttleTimetableView.route_tag.in_(route_tag))
    if stop_name:
        timetable_condition.append(ShuttleTimetableView.stop_name.in_(stop_name))
    if start:
        timetable_condition.append(
            ShuttleTimetableView.departure_time >= start.replace(
                tzinfo=KST,
            ),
        )
    if end:
        timetable_condition.append(
            ShuttleTimetableView.departure_time <= end.replace(
                tzinfo=KST,
            ),
        )
    select_query = (
        select(ShuttleTimetableView)
        .options(
            load_only(
                ShuttleTimetableView.id_,
                ShuttleTimetableView.period,
                ShuttleTimetableView.is_weekdays,
                ShuttleTimetableView.route_name,
                ShuttleTimetableView.route_tag,
                ShuttleTimetableView.stop_name,
                ShuttleTimetableView.departure_time,
            ),
            selectinload(ShuttleTimetableView.via).options(
                load_only(
                    ShuttleTimetableView.stop_name,
                    ShuttleTimetableView.departure_time,
                ),
            ),
        )
        .where(and_(*timetable_condition))
        .order_by(ShuttleTimetableView.id_)
    )
    timetable_list = await fetch_all(select_query)
    return [
        ShuttleTimetableQuery(
            id_=timetable.id_,
            period=timetable.period,
            is_weekdays=timetable.is_weekdays,
            route_name=timetable.route_name,
            route_tag=timetable.route_tag,
            stop_name=timetable.stop_name,
            departure_time=timetable.departure_time.strftime("%H:%M:%S"),
            departure_hour=timetable.departure_time.hour,
            departure_minute=timetable.departure_time.minute,
            via=[
                ShuttleViaQuery(
                    stop=via.stop_name,
                    departure_time=via.departure_time.strftime("%H:%M:%S"),
                    departure_hour=via.departure_time.hour,
                    departure_minute=via.departure_time.minute
                )
                for via in sorted(timetable.via, key=lambda x: x.departure_time)
            ],
        )
        for timetable in timetable_list
    ]


async def resolve_shuttle_grouped_timetable(
    timestamp: datetime.datetime | None = datetime.datetime.now(tz=pytz.timezone("Asia/Seoul")),
    count: int = 3,
    group: str = "destination",
    period: list[str] | None = None,
    weekdays: list[bool] | None = None,
    route_name: list[str] | None = None,
    route_tag: list[str] | None = None,
    stop_name: list[str] | None = None,
    start: datetime.time | None = None,
    end: datetime.time | None = None,
) -> list[ShuttleTimetableGroupedQuery]:
    timetable_condition: list[ColumnElement[bool] | ColumnElement[bool]] = []
    if period:
        timetable_condition.append(ShuttleTimetableGroupedView.period.in_(period))
    elif timestamp:
        select_period_query = (
            select(ShuttlePeriod)
            .options(load_only(ShuttlePeriod.type_id))
            .where(
                and_(
                    ShuttlePeriod.start <= timestamp,
                    ShuttlePeriod.end >= timestamp,
                ),
            )
            .order_by(ShuttlePeriod.type_id.desc())
        )
        current_period = await fetch_one(select_period_query)
        if current_period is None:
            raise PeriodNotFound()
        timetable_condition.append(
            ShuttleTimetableGroupedView.period == current_period.type_id,
        )
    if weekdays == [True]:
        timetable_condition.append(ShuttleTimetableGroupedView.is_weekdays.is_(true()))
    elif weekdays == [False]:
        timetable_condition.append(ShuttleTimetableGroupedView.is_weekdays.is_(false()))
    elif weekdays is None and timestamp:
        lunar_calendar.setSolarDate(timestamp.year, timestamp.month, timestamp.day)
        lunar_date = lunar_calendar.LunarIsoFormat()
        try:
            formatted_lunar_date = datetime.date.fromisoformat(lunar_date)
            select_holiday_query = (
                select(ShuttleHoliday)
                .options(load_only(ShuttleHoliday.type_))
                .where(
                    or_(
                        and_(
                            ShuttleHoliday.date == timestamp.date(),
                            ShuttleHoliday.calendar == "solar",
                        ),
                        and_(
                            ShuttleHoliday.date == formatted_lunar_date,
                            ShuttleHoliday.calendar == "lunar",
                        ),
                    ),
                )
            )
        except ValueError:
            select_holiday_query = (
                select(ShuttleHoliday)
                .options(load_only(ShuttleHoliday.type_))
                .where(
                    and_(
                        ShuttleHoliday.date == timestamp.date(),
                        ShuttleHoliday.calendar == "solar",
                    ),
                )
            )

        holiday = await fetch_one(select_holiday_query)
        if holiday is not None:
            if holiday.type_ == "weekends":
                timetable_condition.append(
                    ShuttleTimetableGroupedView.is_weekdays.is_(false()),
                )
            elif holiday.type_ == "halt":
                return []
        else:
            if timestamp.isoformat() in kr_holidays:
                timetable_condition.append(
                    ShuttleTimetableGroupedView.is_weekdays.is_(false()))
            elif timestamp.weekday() >= 5:
                timetable_condition.append(ShuttleTimetableGroupedView.is_weekdays.is_(false()))
            else:
                timetable_condition.append(ShuttleTimetableGroupedView.is_weekdays.is_(true()))
    if route_name:
        timetable_condition.append(ShuttleTimetableGroupedView.route_name.in_(route_name))
    if route_tag:
        timetable_condition.append(ShuttleTimetableGroupedView.route_tag.in_(route_tag))
    if stop_name:
        timetable_condition.append(ShuttleTimetableGroupedView.stop_name.in_(stop_name))
    if start:
        timetable_condition.append(
            ShuttleTimetableGroupedView.departure_time >= start.replace(
                tzinfo=KST,
            ),
        )
    if end:
        timetable_condition.append(
            ShuttleTimetableGroupedView.departure_time <= end.replace(
                tzinfo=KST,
            ),
        )
    timetable_list: list[ShuttleTimetableGroupedView] = []
    if group == "destination":
        timetable_subquery = (
            select(
                ShuttleTimetableGroupedView,
                func.row_number().over(
                    partition_by=(
                        ShuttleTimetableGroupedView.stop_name,
                        ShuttleTimetableGroupedView.destination_group
                    ),
                    order_by=ShuttleTimetableGroupedView.departure_time.asc()
                ).label("rn")
            )
            .where(and_(*timetable_condition))
            .subquery()
        )
        aliased_subquery = aliased(ShuttleTimetableGroupedView, timetable_subquery)
        # 메인 쿼리: rn <= 1 조건 필터링 및 정렬
        ranked_shuttles_query = (
            select(aliased_subquery)
            .select_from(aliased_subquery)
            .where(timetable_subquery.c.rn <= count)
            .order_by(
                timetable_subquery.c.stop_name,
                timetable_subquery.c.destination_group,
                timetable_subquery.c.departure_time
            )
        )
        timetable_list = await fetch_all(ranked_shuttles_query)
    else:
        timetable_subquery = (
            select(
                ShuttleTimetableGroupedView,
                func.row_number().over(
                    partition_by=(ShuttleTimetableGroupedView.stop_name),
                    order_by=ShuttleTimetableGroupedView.departure_time.asc()
                ).label("rn")
            )
            .where(and_(*timetable_condition))
            .subquery()
        )
        aliased_subquery = aliased(ShuttleTimetableGroupedView, timetable_subquery)
        # 메인 쿼리: rn <= 1 조건 필터링 및 정렬
        ranked_shuttles_query = (
            select(aliased_subquery)
            .select_from(aliased_subquery)
            .where(timetable_subquery.c.rn <= count)
            .order_by(
                timetable_subquery.c.stop_name,
                timetable_subquery.c.destination_group,
                timetable_subquery.c.departure_time
            )
        )
        timetable_list = await fetch_all(ranked_shuttles_query)
    return [
        ShuttleTimetableGroupedQuery(
            id_=timetable.id_,
            period=timetable.period,
            is_weekdays=timetable.is_weekdays,
            route_name=timetable.route_name,
            route_tag=timetable.route_tag,
            stop_name=timetable.stop_name,
            departure_time=timetable.departure_time.strftime("%H:%M:%S"),
            departure_hour=timetable.departure_time.hour,
            departure_minute=timetable.departure_time.minute,
            destination_group=timetable.destination_group,
        )
        for timetable in timetable_list
    ]


async def resolve_shuttle_period(
    start: datetime.date | None = None,
    end: datetime.date | None = None,
    current: bool | None = None,
) -> list[ShuttlePeriodQuery]:
    period_condition = []
    if current is True:
        now = datetime.datetime.now().astimezone(tz=timezone("Asia/Seoul"))
        period_condition.append(ShuttlePeriod.start <= now)
        period_condition.append(ShuttlePeriod.end >= now)
    else:
        if start:
            period_condition.append(ShuttlePeriod.start <= start)
        if end:
            period_condition.append(ShuttlePeriod.end >= end)

    if period_condition:
        select_query = select(ShuttlePeriod).where(and_(*period_condition))
    else:
        select_query = select(ShuttlePeriod)
    period_list = await fetch_all(select_query)
    return [
        ShuttlePeriodQuery(
            start=period.start.astimezone(tz=timezone("Asia/Seoul")),
            end=period.end.astimezone(tz=timezone("Asia/Seoul")),
            type_=period.type_id,
        )
        for period in period_list
    ]


async def resolve_shuttle_holiday() -> list[ShuttleHolidayQuery]:
    select_query = select(ShuttleHoliday)
    holiday = await fetch_all(select_query)
    return [
        ShuttleHolidayQuery(
            date=holiday.date,
            calendar=holiday.calendar,
            type_=holiday.type_,
        )
        for holiday in holiday
    ]


async def resolve_shuttle_stop(
    stop_name: list[str] | None = None,
) -> list[ShuttleStopQuery]:
    select_query = (
        select(ShuttleStop)
        .options(
            load_only(
                ShuttleStop.name,
                ShuttleStop.latitude,
                ShuttleStop.longitude,
            ),
            selectinload(ShuttleStop.routes).options(
                joinedload(ShuttleRouteStop.route).options(
                    load_only(
                        ShuttleRoute.name,
                        ShuttleRoute.tag,
                        ShuttleRoute.start_stop_id,
                        ShuttleRoute.end_stop_id,
                        ShuttleRoute.korean,
                        ShuttleRoute.english,
                    ),
                ),
            ),
        )
    )
    if stop_name:
        select_query = select_query.where(ShuttleStop.name.in_(stop_name))
    stop_list = await fetch_all(select_query)
    return [
        ShuttleStopQuery(
            name=stop.name,
            latitude=stop.latitude,
            longitude=stop.longitude,
            routes=[
                ShuttleStopRouteQuery(
                    name=route.route.name,
                    tag=route.route.tag,
                    start=route.route.start_stop_id,
                    end=route.route.end_stop_id,
                    korean=route.route.korean,
                    english=route.route.english,
                )
                for route in stop.routes
            ],
        )
        for stop in stop_list
    ]


async def resolve_shuttle_route(
    route_name: list[str] | None = None,
    route_tag: list[str] | None = None,
    start_stop: list[str] | None = None,
    end_stop: list[str] | None = None,
) -> list[ShuttleRouteQuery]:
    route_condition = []
    if route_name:
        route_condition.append(ShuttleRoute.name.in_(route_name))
    if route_tag:
        route_condition.append(ShuttleRoute.tag.in_(route_tag))
    if start_stop:
        route_condition.append(ShuttleRoute.start_stop_id.in_(start_stop))
    if end_stop:
        route_condition.append(ShuttleRoute.end_stop_id.in_(end_stop))
    select_query = (
        select(ShuttleRoute)
        .options(
            load_only(
                ShuttleRoute.name,
                ShuttleRoute.tag,
                ShuttleRoute.start_stop_id,
                ShuttleRoute.end_stop_id,
                ShuttleRoute.korean,
                ShuttleRoute.english,
            ),
            selectinload(ShuttleRoute.stops).options(
                load_only(
                    ShuttleRouteStop.stop_name,
                    ShuttleRouteStop.sequence,
                ),
            ),
        )
    )
    if route_condition:
        select_query = select_query.where(and_(*route_condition))
    route_list = await fetch_all(select_query)
    return [
        ShuttleRouteQuery(
            name=route.name,
            tag=route.tag,
            start=route.start_stop_id,
            end=route.end_stop_id,
            korean=route.korean,
            english=route.english,
            stops=[
                ShuttleRouteStopQuery(
                    name=stop.stop_name,
                    sequence=stop.sequence,
                )
                for stop in sorted(route.stops, key=lambda x: x.sequence)
            ],
        )
        for route in route_list
    ]
