from typing import List

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model import Base
from model.cafeteria import Cafeteria
from model.reading_room import ReadingRoom


class Campus(Base):
    __tablename__ = "campus"

    id_: Mapped[int] = mapped_column("campus_id", Integer, primary_key=True)
    name: Mapped[str] = mapped_column("campus_name", String(30))

    cafeteria_list: Mapped[List["Cafeteria"]] = relationship(
        back_populates="campus",
        cascade="all, delete-orphan",
        viewonly=True,
    )
    reading_room_list: Mapped[List["ReadingRoom"]] = relationship(
        back_populates="campus",
        cascade="all, delete-orphan",
        viewonly=True,
    )
