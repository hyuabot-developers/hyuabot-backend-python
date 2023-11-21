import datetime
from typing import List

from sqlalchemy import String, DateTime, PrimaryKeyConstraint, Time, Boolean, Interval, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.model import Base


class ShuttlePeriodType(Base):
    __tablename__ = "shuttle_period_type"

    type: Mapped[str] = mapped_column("period_type", String(20), primary_key=True)
    periods: Mapped["List[ShuttlePeriod]"] = relationship(
        "ShuttlePeriod",
        back_populates="type",
        cascade="all, delete-orphan",
    )


class ShuttlePeriod(Base):
    __tablename__ = "shuttle_period"
    __table_args__ = (
        PrimaryKeyConstraint(
            "period_type", "period_start", "period_end",
            name="pk_shuttle_period",
        ),
    )

    type: Mapped[str] = mapped_column("period_type", String(20))
    start: Mapped[datetime.datetime] = mapped_column("period_start", DateTime)
    end: Mapped[datetime.datetime] = mapped_column("period_end", DateTime)


class ShuttleRoute(Base):
    __tablename__ = "shuttle_route"

    name: Mapped[str] = mapped_column("route_name", String(15), primary_key=True)
    korean: Mapped[str] = mapped_column("route_description_korean", String(100))
    english: Mapped[str] = mapped_column("route_description_english", String(100))
    tag: Mapped[str] = mapped_column("route_tag", String(10))
    start_stop_id: Mapped[str] = mapped_column("start_stop", String(15))
    end_stop_id: Mapped[str] = mapped_column("end_stop", String(15))

    start_stop: Mapped["ShuttleStop"] = relationship("ShuttleStop")
    end_stop: Mapped["ShuttleStop"] = relationship("ShuttleStop")
    timetable: Mapped[List["ShuttleTimetable"]] = relationship(
        "ShuttleTimetable",
        back_populates="route",
        cascade="all, delete-orphan",
    )
    stops: Mapped[List["ShuttleRouteStop"]] = relationship(
        "ShuttleRouteStop",
        back_populates="route",
        cascade="all, delete-orphan",
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
    )


class ShuttleRouteStop(Base):
    __tablename__ = "shuttle_route_stop"
    __table_args__ = (
        PrimaryKeyConstraint(
            "route_name", "stop_name",
            name="pk_shuttle_route_stop",
        ),
    )

    route_name: Mapped[str] = mapped_column("route_name", String(15))
    stop_name: Mapped[str] = mapped_column("stop_name", String(15))
    sequence: Mapped[int] = mapped_column("stop_order", Integer)
    cumulative_time: Mapped[datetime.timedelta] = mapped_column("cumulative_time", Interval)

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

    id: Mapped[int] = mapped_column("seq", Integer, primary_key=True)
    period: Mapped[str] = mapped_column("period_type", String(20))
    is_weekdays: Mapped[bool] = mapped_column("weekday", Boolean)
    route_name: Mapped[str] = mapped_column("route_name", String(15))
    departure_time: Mapped[datetime.time] = mapped_column("departure_time", Time)


class ShuttleTimetableView(Base):
    __tablename__ = "shuttle_timetable_view"
    __table_args__ = (
        PrimaryKeyConstraint(
            "seq", "stop_name",
            name="pk_shuttle_timetable_view",
        ),
        {'info': dict(is_view=True)},
    )

    id: Mapped[int] = mapped_column("seq", Integer)
    period: Mapped[str] = mapped_column("period_type", String(20))
    is_weekdays: Mapped[bool] = mapped_column("weekday", Boolean)
    route_name: Mapped[str] = mapped_column("route_name", String(15))
    route_tag: Mapped[str] = mapped_column("route_tag", String(10))
    stop_name: Mapped[str] = mapped_column("stop_name", String(15))
    departure_time: Mapped[datetime.time] = mapped_column("departure_time", Time)
