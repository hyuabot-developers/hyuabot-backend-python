import datetime
from typing import List

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    Integer,
    Interval,
    PrimaryKeyConstraint,
    String,
    Time,
    Date,
    ForeignKeyConstraint,
    Sequence,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model import Base


class ShuttlePeriodType(Base):
    __tablename__ = "shuttle_period_type"

    type_: Mapped[str] = mapped_column("period_type", String(20), primary_key=True)
    periods: Mapped["List[ShuttlePeriod]"] = relationship(
        "ShuttlePeriod",
        back_populates="type_",
        cascade="all, delete-orphan",
        viewonly=True,
    )


class ShuttlePeriod(Base):
    __tablename__ = "shuttle_period"
    __table_args__ = (
        PrimaryKeyConstraint(
            "period_type",
            "period_start",
            "period_end",
            name="pk_shuttle_period",
        ),
        ForeignKeyConstraint(
            ["period_type"],
            ["shuttle_period_type.period_type"],
            name="fk_shuttle_period_type",
        ),
    )

    type_id: Mapped[str] = mapped_column("period_type", String(20))
    start: Mapped[datetime.datetime] = mapped_column(
        "period_start",
        DateTime(timezone=True),
    )
    end: Mapped[datetime.datetime] = mapped_column(
        "period_end",
        DateTime(timezone=True),
    )

    type_: Mapped["ShuttlePeriodType"] = relationship(
        "ShuttlePeriodType",
        back_populates="periods",
    )


class ShuttleHoliday(Base):
    __tablename__ = "shuttle_holiday"
    __table_args__ = (
        PrimaryKeyConstraint(
            "holiday_date",
            "holiday_type",
            "calendar_type",
            name="pk_shuttle_holiday",
        ),
    )

    date: Mapped[datetime.date] = mapped_column("holiday_date", Date)
    type_: Mapped[str] = mapped_column("holiday_type", String(15))
    calendar: Mapped[str] = mapped_column("calendar_type", String(15))


class ShuttleRoute(Base):
    __tablename__ = "shuttle_route"
    __table_args__ = (
        ForeignKeyConstraint(
            ["start_stop"],
            ["shuttle_stop.stop_name"],
            name="fk_shuttle_route_start_stop",
        ),
        ForeignKeyConstraint(
            ["end_stop"],
            ["shuttle_stop.stop_name"],
            name="fk_shuttle_route_end_stop",
        ),
    )

    name: Mapped[str] = mapped_column("route_name", String(15), primary_key=True)
    korean: Mapped[str] = mapped_column("route_description_korean", String(100))
    english: Mapped[str] = mapped_column("route_description_english", String(100))
    tag: Mapped[str] = mapped_column("route_tag", String(10))
    start_stop_id: Mapped[str] = mapped_column("start_stop", String(15))
    end_stop_id: Mapped[str] = mapped_column("end_stop", String(15))

    start_stop: Mapped["ShuttleStop"] = relationship(
        "ShuttleStop",
        primaryjoin="ShuttleRoute.start_stop_id == ShuttleStop.name",
    )
    end_stop: Mapped["ShuttleStop"] = relationship(
        "ShuttleStop",
        primaryjoin="ShuttleRoute.end_stop_id == ShuttleStop.name",
    )
    timetable: Mapped[List["ShuttleTimetable"]] = relationship(
        "ShuttleTimetable",
        back_populates="route",
        cascade="all, delete-orphan",
        viewonly=True,
    )
    stops: Mapped[List["ShuttleRouteStop"]] = relationship(
        "ShuttleRouteStop",
        back_populates="route",
        cascade="all, delete-orphan",
        viewonly=True,
    )


class ShuttleStop(Base):
    __tablename__ = "shuttle_stop"

    name: Mapped[str] = mapped_column("stop_name", String(15), primary_key=True)
    latitude: Mapped[float] = mapped_column("latitude", Float)
    longitude: Mapped[float] = mapped_column("longitude", Float)

    routes: Mapped[List["ShuttleRouteStop"]] = relationship(
        "ShuttleRouteStop",
        back_populates="stop",
        cascade="all, delete-orphan",
        viewonly=True,
    )


class ShuttleRouteStop(Base):
    __tablename__ = "shuttle_route_stop"
    __table_args__ = (
        PrimaryKeyConstraint(
            "route_name",
            "stop_name",
            name="pk_shuttle_route_stop",
        ),
        ForeignKeyConstraint(
            ["route_name"],
            ["shuttle_route.route_name"],
            name="fk_shuttle_route_stop_route",
        ),
        ForeignKeyConstraint(
            ["stop_name"],
            ["shuttle_stop.stop_name"],
            name="fk_shuttle_route_stop_stop",
        ),
    )

    route_name: Mapped[str] = mapped_column("route_name", String(15))
    stop_name: Mapped[str] = mapped_column("stop_name", String(15))
    sequence: Mapped[int] = mapped_column("stop_order", Integer)
    cumulative_time: Mapped[datetime.timedelta] = mapped_column(
        "cumulative_time",
        Interval,
    )

    route: Mapped["ShuttleRoute"] = relationship(
        "ShuttleRoute",
        back_populates="stops",
    )
    stop: Mapped["ShuttleStop"] = relationship(
        "ShuttleStop",
        back_populates="routes",
    )


class ShuttleTimetable(Base):
    __tablename__ = "shuttle_timetable"
    __table_args__ = (
        ForeignKeyConstraint(
            ["route_name"],
            ["shuttle_route.route_name"],
            name="fk_shuttle_timetable_route",
        ),
    )

    id_: Mapped[int] = mapped_column(
        "seq",
        Integer,
        Sequence("shuttle_timetable_seq_seq"),
        primary_key=True,
    )
    period: Mapped[str] = mapped_column("period_type", String(20))
    is_weekdays: Mapped[bool] = mapped_column("weekday", Boolean)
    route_name: Mapped[str] = mapped_column("route_name", String(15))
    departure_time: Mapped[datetime.time] = mapped_column("departure_time", Time)

    route: Mapped["ShuttleRoute"] = relationship(
        "ShuttleRoute",
        back_populates="timetable",
    )


class ShuttleTimetableView(Base):
    __tablename__ = "shuttle_timetable_view"
    __table_args__ = (
        PrimaryKeyConstraint(
            "seq",
            "stop_name",
            name="pk_shuttle_timetable_view",
        ),
        ForeignKeyConstraint(
            ["seq"],
            ["shuttle_timetable_view.seq"],
            name="fk_shuttle_timetable_view_timetable",
        ),
        {"info": dict(is_view=True)},
    )

    id_: Mapped[int] = mapped_column("seq", Integer)
    period: Mapped[str] = mapped_column("period_type", String(20))
    is_weekdays: Mapped[bool] = mapped_column("weekday", Boolean)
    route_name: Mapped[str] = mapped_column("route_name", String(15))
    route_tag: Mapped[str] = mapped_column("route_tag", String(10))
    stop_name: Mapped[str] = mapped_column("stop_name", String(15))
    departure_time: Mapped[datetime.time] = mapped_column(
        "departure_time",
        Time,
    )
    via: Mapped[list["ShuttleTimetableView"]] = relationship(
        "ShuttleTimetableView",
        remote_side=[id_],
        viewonly=True,
    )
