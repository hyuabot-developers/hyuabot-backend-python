import datetime
from typing import List

from sqlalchemy import String, Time, PrimaryKeyConstraint, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base


class CommuteShuttleRoute(Base):
    __tablename__ = "commute_shuttle_route"

    name: Mapped[str] = mapped_column("route_name", String(15), primary_key=True)
    korean: Mapped[str] = mapped_column("route_description_korean", String(100))
    english: Mapped[str] = mapped_column("route_description_english", String(100))

    timetable: Mapped[List["CommuteShuttleTimetable"]] = relationship(
        "CommuteShuttleTimetable",
        back_populates="route",
        cascade="all, delete-orphan",
    )


class CommuteShuttleStop(Base):
    __tablename__ = "commute_shuttle_stop"

    name: Mapped[str] = mapped_column("stop_name", primary_key=True)
    description: Mapped[str] = mapped_column("description", String(50))
    latitude: Mapped[float] = mapped_column("latitude", Float)
    longitude: Mapped[float] = mapped_column("longitude", Float)

    timetable: Mapped[List["CommuteShuttleTimetable"]] = relationship(
        "CommuteShuttleTimetable",
        back_populates="stop",
        cascade="all, delete-orphan",
    )


class CommuteShuttleTimetable(Base):
    __tablename__ = "commute_shuttle_timetable"
    __table_args__ = (
        PrimaryKeyConstraint(
            "route_name", "stop_name",
            name="pk_commute_shuttle_timetable",
        ),
    )

    route_name: Mapped[str] = mapped_column("route_name", String(15))
    stop_name: Mapped[str] = mapped_column("stop_name", String(50))
    sequence: Mapped[int] = mapped_column("stop_order", Integer)
    time: Mapped[datetime.time] = mapped_column("departure_time", Time)

    route: Mapped["CommuteShuttleRoute"] = relationship(
        "CommuteShuttleRoute",
        back_populates="timetable",
    )

    stop: Mapped["CommuteShuttleStop"] = relationship(
        "CommuteShuttleStop",
        back_populates="timetable",
    )
