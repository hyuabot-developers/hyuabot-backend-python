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
    ForeignKeyConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model import Base


class BusTimetable(Base):
    __tablename__ = "bus_timetable"
    __table_args__ = (
        PrimaryKeyConstraint(
            "route_id",
            "start_stop_id",
            "weekday",
            "departure_time",
            name="pk_bus_timetable",
        ),
        ForeignKeyConstraint(
            ["route_id"],
            ["bus_route.route_id"],
            name="fk_bus_timetable_route_id",
        ),
        ForeignKeyConstraint(
            ["start_stop_id"],
            ["bus_stop.stop_id"],
            name="fk_bus_timetable_start_stop_id",
        ),
        ForeignKeyConstraint(
            ["route_id", "start_stop_id"],
            ["bus_route_stop.route_id", "bus_route_stop.start_stop_id"],
            name="fk_bus_timetable_route_stop",
        ),
    )

    route_id: Mapped[int] = mapped_column("route_id", Integer)
    start_stop_id: Mapped[int] = mapped_column("start_stop_id", Integer)
    weekday: Mapped[str] = mapped_column("weekday", String(10))
    departure_time: Mapped[datetime.time] = mapped_column(
        "departure_time",
        Time(timezone=True),
    )

    route: Mapped["BusRoute"] = relationship(
        "BusRoute",
        back_populates="timetable",
    )


class BusRealtime(Base):
    __tablename__ = "bus_realtime"
    __table_args__ = (
        PrimaryKeyConstraint(
            "stop_id",
            "route_id",
            "arrival_sequence",
            name="pk_bus_realtime",
        ),
        ForeignKeyConstraint(
            ["route_id", "stop_id"],
            ["bus_route_stop.route_id", "bus_route_stop.stop_id"],
            name="fk_bus_realtime_route_stop",
        ),
    )

    stop_id: Mapped[int] = mapped_column("stop_id", Integer)
    route_id: Mapped[int] = mapped_column("route_id", Integer)
    sequence: Mapped[int] = mapped_column("arrival_sequence", Integer)
    stops: Mapped[int] = mapped_column("remaining_stop_count", Integer)
    seats: Mapped[int] = mapped_column("remaining_seat_count", Integer)
    time: Mapped[datetime.timedelta] = mapped_column("remaining_time", Interval)
    low_floor: Mapped[bool] = mapped_column("low_plate", Boolean)
    updated_at: Mapped[datetime.datetime] = mapped_column(
        "last_updated_time",
        DateTime(timezone=True),
    )


class BusRouteStop(Base):
    __tablename__ = "bus_route_stop"
    __table_args__ = (
        PrimaryKeyConstraint(
            "route_id",
            "stop_id",
            name="pk_bus_route_stop",
        ),
        ForeignKeyConstraint(
            ["route_id"],
            ["bus_route.route_id"],
            name="fk_bus_route_stop_route_id",
        ),
        ForeignKeyConstraint(
            ["stop_id"],
            ["bus_stop.stop_id"],
            name="fk_bus_route_stop_stop_id",
        ),
        ForeignKeyConstraint(
            ["start_stop_id"],
            ["bus_stop.stop_id"],
            name="fk_bus_route_stop_start_stop_id",
        ),
    )

    route_id: Mapped[int] = mapped_column("route_id", Integer)
    stop_id: Mapped[int] = mapped_column("stop_id", Integer)
    sequence: Mapped[int] = mapped_column("stop_sequence", Integer)
    start_stop_id: Mapped[int] = mapped_column("start_stop_id", Integer)

    route: Mapped["BusRoute"] = relationship(
        "BusRoute",
        back_populates="stops",
    )
    stop: Mapped["BusStop"] = relationship(
        "BusStop",
        primaryjoin="BusRouteStop.stop_id == BusStop.id_",
    )
    start_stop: Mapped["BusStop"] = relationship(
        "BusStop",
        back_populates="start_routes",
        primaryjoin="BusRouteStop.start_stop_id == BusStop.id_",
    )
    timetable: Mapped[List["BusTimetable"]] = relationship(
        "BusTimetable",
        cascade="all, delete-orphan",
        primaryjoin=(
            "and_(BusRouteStop.route_id == BusTimetable.route_id, "
            "BusRouteStop.start_stop_id == BusTimetable.start_stop_id)"
        ),
        viewonly=True,
    )
    realtime: Mapped[List["BusRealtime"]] = relationship(
        "BusRealtime",
        cascade="all, delete-orphan",
        primaryjoin=(
            "and_(BusRouteStop.route_id == BusRealtime.route_id, "
            "BusRouteStop.stop_id == BusRealtime.stop_id)"
        ),
        viewonly=True,
    )


class BusRoute(Base):
    __tablename__ = "bus_route"
    __table_args__ = (
        ForeignKeyConstraint(
            ["start_stop_id"],
            ["bus_stop.stop_id"],
            name="fk_bus_route_start_stop_id",
        ),
        ForeignKeyConstraint(
            ["end_stop_id"],
            ["bus_stop.stop_id"],
            name="fk_bus_route_end_stop_id",
        ),
    )

    id_: Mapped[int] = mapped_column("route_id", Integer, primary_key=True)
    name: Mapped[str] = mapped_column("route_name", String(30))
    type_code: Mapped[str] = mapped_column("route_type_code", String(10))
    type_name: Mapped[str] = mapped_column("route_type_name", String(10))
    company_id: Mapped[int] = mapped_column("company_id", Integer)
    company_name: Mapped[str] = mapped_column("company_name", String(30))
    company_telephone: Mapped[str] = mapped_column("company_telephone", String(15))
    district: Mapped[int] = mapped_column("district_code", Integer)
    up_first_time: Mapped[datetime.time] = mapped_column(
        "up_first_time",
        Time(timezone=True),
    )
    up_last_time: Mapped[datetime.time] = mapped_column(
        "up_last_time",
        Time(timezone=True),
    )
    down_first_time: Mapped[datetime.time] = mapped_column(
        "down_first_time",
        Time(timezone=True),
    )
    down_last_time: Mapped[datetime.time] = mapped_column(
        "down_last_time",
        Time(timezone=True),
    )
    start_stop_id: Mapped[int] = mapped_column("start_stop_id", Integer)
    end_stop_id: Mapped[int] = mapped_column("end_stop_id", Integer)

    stops: Mapped[List["BusRouteStop"]] = relationship(
        "BusRouteStop",
        back_populates="route",
        cascade="all, delete-orphan",
        viewonly=True,
    )
    timetable: Mapped[List["BusTimetable"]] = relationship(
        "BusTimetable",
        back_populates="route",
        cascade="all, delete-orphan",
        viewonly=True,
    )
    start_stop: Mapped["BusStop"] = relationship(
        "BusStop",
        primaryjoin="BusRoute.start_stop_id == BusStop.id_",
    )
    end_stop: Mapped["BusStop"] = relationship(
        "BusStop",
        primaryjoin="BusRoute.end_stop_id == BusStop.id_",
    )


class BusStop(Base):
    __tablename__ = "bus_stop"

    id_: Mapped[int] = mapped_column("stop_id", Integer, primary_key=True)
    name: Mapped[str] = mapped_column("stop_name", String(30))
    district: Mapped[int] = mapped_column("district_code", Integer)
    mobile_no: Mapped[str] = mapped_column("mobile_number", String(15))
    region: Mapped[str] = mapped_column("region_name", String(10))
    latitude: Mapped[float] = mapped_column("latitude", Float)
    longitude: Mapped[float] = mapped_column("longitude", Float)

    start_routes: Mapped[List["BusRouteStop"]] = relationship(
        "BusRouteStop",
        back_populates="start_stop",
        cascade="all, delete-orphan",
        primaryjoin="BusStop.id_ == BusRouteStop.start_stop_id",
        viewonly=True,
    )
