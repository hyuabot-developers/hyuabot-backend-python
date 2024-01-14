import datetime
from typing import List

from sqlalchemy import (
    Boolean,
    DateTime,
    Integer,
    Interval,
    PrimaryKeyConstraint,
    String,
    Time,
    ForeignKeyConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model import Base


class SubwayStation(Base):
    __tablename__ = "subway_station"

    name: Mapped[str] = mapped_column("station_name", String(30), primary_key=True)


class SubwayRoute(Base):
    __tablename__ = "subway_route"

    _id: Mapped[int] = mapped_column("route_id", Integer, primary_key=True)
    name: Mapped[str] = mapped_column("route_name", String(30))


class SubwayRouteStation(Base):
    __tablename__ = "subway_route_station"

    _id: Mapped[str] = mapped_column("station_id", String(10), primary_key=True)
    route_id: Mapped[int] = mapped_column("route_id", Integer)
    name: Mapped[str] = mapped_column("station_name", String(30))
    sequence: Mapped[int] = mapped_column("station_sequence", Integer)
    cumulative_time: Mapped[datetime.timedelta] = mapped_column(
        "cumulative_time",
        Interval,
    )

    timetable: Mapped[List["SubwayTimetable"]] = relationship(
        "SubwayTimetable",
        back_populates="station",
        cascade="all, delete-orphan",
        primaryjoin="SubwayRouteStation._id == SubwayTimetable.station_id",
        viewonly=True,
    )
    realtime: Mapped[List["SubwayRealtime"]] = relationship(
        "SubwayRealtime",
        back_populates="station",
        cascade="all, delete-orphan",
        primaryjoin="SubwayRouteStation._id == SubwayRealtime.station_id",
        viewonly=True,
    )


class SubwayTimetable(Base):
    __tablename__ = "subway_timetable"
    __table_args__ = (
        PrimaryKeyConstraint(
            "station_id",
            "up_down_type",
            "weekday",
            "departure_time",
            name="pk_subway_timetable",
        ),
        ForeignKeyConstraint(
            [
                "station_id",
                "start_station_id",
                "terminal_station_id",
            ],
            [
                "subway_route_station.station_id",
                "subway_route_station.station_id",
                "subway_route_station.station_id",
            ],
        ),
    )

    station_id: Mapped[str] = mapped_column("station_id", String(10))
    heading: Mapped[str] = mapped_column("up_down_type", String(10))
    is_weekdays: Mapped[str] = mapped_column("weekday", String(10))
    departure_time: Mapped[datetime.time] = mapped_column(
        "departure_time",
        Time(timezone=True),
    )
    start_station_id: Mapped[str] = mapped_column("start_station_id", String(10))
    terminal_station_id: Mapped[str] = mapped_column("terminal_station_id", String(10))

    station: Mapped["SubwayRouteStation"] = relationship(
        "SubwayRouteStation",
        back_populates="timetable",
    )


class SubwayRealtime(Base):
    __tablename__ = "subway_realtime"
    __table_args__ = (
        PrimaryKeyConstraint(
            "station_id",
            "up_down_type",
            "arrival_sequence",
            name="pk_subway_realtime",
        ),
        ForeignKeyConstraint(
            ["station_id", "terminal_station_id"],
            ["subway_route_station.station_id", "subway_route_station.station_id"],
        ),
    )

    station_id: Mapped[str] = mapped_column("station_id", String(10))
    heading: Mapped[str] = mapped_column("up_down_type", String(10))
    sequence: Mapped[int] = mapped_column("arrival_sequence", Integer)
    location: Mapped[str] = mapped_column("current_station_name", String(30))
    stop: Mapped[int] = mapped_column("remaining_stop_count", Integer)
    time: Mapped[datetime.timedelta] = mapped_column("remaining_time", Interval)
    terminal_station_id: Mapped[str] = mapped_column("terminal_station_id", String(10))
    train_number: Mapped[str] = mapped_column("train_number", String(10))
    is_express: Mapped[bool] = mapped_column("is_express_train", Boolean)
    is_last: Mapped[bool] = mapped_column("is_last_train", Boolean)
    status: Mapped[int] = mapped_column("status_code", Integer)
    updated_at: Mapped[datetime.datetime] = mapped_column(
        "last_updated_time",
        DateTime(timezone=True),
        default=datetime.datetime.now,
    )

    station: Mapped["SubwayRouteStation"] = relationship(
        "SubwayRouteStation",
        back_populates="realtime",
        primaryjoin="SubwayRealtime.station_id == SubwayRouteStation._id",
    )
    terminal_station: Mapped["SubwayRouteStation"] = relationship(
        "SubwayRouteStation",
        primaryjoin="SubwayRealtime.terminal_station_id == SubwayRouteStation._id",
    )
