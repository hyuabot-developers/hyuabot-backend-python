from sqlalchemy import ForeignKeyConstraint, Integer, Float, Text, String
from sqlalchemy.orm import Mapped, mapped_column

from model import Base


class Building(Base):
    __tablename__ = "building"
    __table_args__ = (
        ForeignKeyConstraint(
            ["campus_id"],
            ["campus.campus_id"],
        ),
    )

    id: Mapped[str] = mapped_column("id", String(15), primary_key=True)
    name: Mapped[str] = mapped_column("name", String(30))
    campus_id: Mapped[int] = mapped_column("campus_id", Integer)
    latitude: Mapped[float] = mapped_column("latitude", Float)
    longitude: Mapped[float] = mapped_column("longitude", Float)
    url: Mapped[str] = mapped_column("url", Text)


class Room(Base):
    __tablename__ = "room"
    __table_args__ = (
        ForeignKeyConstraint(
            ["building_id"],
            ["building.id"],
        ),
    )

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    building_id: Mapped[str] = mapped_column("building_id", String(15))
    name: Mapped[str] = mapped_column("name", String(30))
    floor: Mapped[str] = mapped_column("floor", String(10))
    number: Mapped[str] = mapped_column("number", String(10))
