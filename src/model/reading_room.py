import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model import Base

if TYPE_CHECKING:
    from model.campus import Campus


class ReadingRoom(Base):
    __tablename__ = "reading_room"

    id: Mapped[int] = mapped_column("room_id", Integer, primary_key=True)
    campus_id: Mapped[int] = mapped_column("campus_id", Integer)
    name: Mapped[str] = mapped_column("room_name", String(30))
    active: Mapped[bool] = mapped_column("is_active", Boolean, default=False)
    reservable: Mapped[bool] = mapped_column("is_reservable", Boolean, default=False)
    total_seats: Mapped[int] = mapped_column("total", Integer, default=0)
    active_total_seats: Mapped[int] = mapped_column("active_total", Integer, default=0)
    occupied_seats: Mapped[int] = mapped_column("occupied", Integer, default=0)
    available_seats: Mapped[int] = mapped_column("available", Integer, default=0)
    updated_at: Mapped[datetime.datetime] = mapped_column(
        "last_updated",
        DateTime,
        default=datetime.datetime.now,
    )

    campus: Mapped["Campus"] = relationship(back_populates="reading_room_list")
