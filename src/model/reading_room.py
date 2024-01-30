import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model import Base

if TYPE_CHECKING:
    from model.campus import Campus


class ReadingRoom(Base):
    __tablename__ = "reading_room"

    id_: Mapped[int] = mapped_column("room_id", Integer, primary_key=True)
    campus_id: Mapped[int] = mapped_column(
        "campus_id",
        Integer,
        ForeignKey("campus.campus_id"),
    )
    name: Mapped[str] = mapped_column("room_name", String(30))
    active: Mapped[bool] = mapped_column("is_active", Boolean)
    reservable: Mapped[bool] = mapped_column("is_reservable", Boolean)
    total_seats: Mapped[int] = mapped_column("total", Integer, default=0)
    active_total_seats: Mapped[int] = mapped_column("active_total", Integer, default=0)
    occupied_seats: Mapped[int] = mapped_column("occupied", Integer, default=0)
    available_seats: Mapped[int] = mapped_column("available", Integer)
    updated_at: Mapped[datetime.datetime] = mapped_column(
        "last_updated_time",
        DateTime(timezone=True),
        default=datetime.datetime.now,
    )

    campus: Mapped["Campus"] = relationship(back_populates="reading_room_list")
