import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import (
    Date,
    Float,
    Integer,
    PrimaryKeyConstraint,
    String,
    ForeignKey,
    ForeignKeyConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model import Base

if TYPE_CHECKING:
    from model.campus import Campus


class Cafeteria(Base):
    __tablename__ = "restaurant"

    id_: Mapped[int] = mapped_column("restaurant_id", Integer, primary_key=True)
    campus_id: Mapped[int] = mapped_column(
        "campus_id",
        Integer,
        ForeignKey("campus.campus_id"),
    )
    name: Mapped[str] = mapped_column("restaurant_name", String(50))
    latitude: Mapped[float] = mapped_column("latitude", Float)
    longitude: Mapped[float] = mapped_column("longitude", Float)

    campus: Mapped["Campus"] = relationship(back_populates="cafeteria_list")
    menu_list: Mapped[List["Menu"]] = relationship(
        back_populates="restaurant",
        cascade="all, delete-orphan",
        viewonly=True,
    )


class Menu(Base):
    __tablename__ = "menu"
    __table_args__ = (
        PrimaryKeyConstraint(
            "restaurant_id",
            "feed_date",
            "time_type",
            name="pk_menu",
        ),
        ForeignKeyConstraint(
            ["restaurant_id"],
            ["restaurant.restaurant_id"],
        ),
    )

    restaurant_id: Mapped[int] = mapped_column(
        "restaurant_id",
        Integer,
        ForeignKey("restaurant.restaurant_id"),
    )
    feed_date: Mapped[datetime.date] = mapped_column("feed_date", Date)
    time_type: Mapped[str] = mapped_column("time_type", String(10))
    menu: Mapped[str] = mapped_column("menu_food", String(400))
    price: Mapped[str] = mapped_column("menu_price", String(30))

    restaurant: Mapped["Cafeteria"] = relationship(
        back_populates="menu_list",
    )
