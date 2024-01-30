from sqlalchemy import (
    ForeignKeyConstraint,
    Integer,
    Float,
    Text,
    String,
    PrimaryKeyConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model import Base


class Building(Base):
    __tablename__ = "building"
    __table_args__ = (
        ForeignKeyConstraint(
            ["campus_id"],
            ["campus.campus_id"],
        ),
    )

    id_: Mapped[str] = mapped_column("id", String(15), primary_key=True)
    name: Mapped[str] = mapped_column("name", String(30))
    campus_id: Mapped[int] = mapped_column("campus_id", Integer)
    latitude: Mapped[float] = mapped_column("latitude", Float)
    longitude: Mapped[float] = mapped_column("longitude", Float)
    url: Mapped[str] = mapped_column("url", Text)
    rooms: Mapped[list["Room"]] = relationship(
        "Room",
        primaryjoin="Building.name == Room.building_name",
    )


class Room(Base):
    __tablename__ = "room"
    __table_args__ = (
        ForeignKeyConstraint(
            ["building_name"],
            ["building.name"],
        ),
        PrimaryKeyConstraint(
            "building_name",
            "number",
            name="pk_room",
        ),
    )

    building_name: Mapped[str] = mapped_column("building_name", String(15))
    name: Mapped[str] = mapped_column("name", String(30))
    number: Mapped[str] = mapped_column("number", String(10))
