import datetime
from typing import List

from sqlalchemy import Sequence, Integer, String, ForeignKeyConstraint, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model import Base


class CalendarCategory(Base):
    __tablename__ = "academic_calendar_category"

    id_: Mapped[int] = mapped_column(
        "category_id",
        Integer,
        Sequence("academic_calendar_category_category_id_seq"),
        primary_key=True,
    )
    name: Mapped[str] = mapped_column("category_name", String(30))
    events: Mapped["List[Calendar]"] = relationship(
        "Calendar",
        cascade="all, delete-orphan",
        primaryjoin="Calendar.category_id == CalendarCategory.id_",
        viewonly=True,
        uselist=True,
    )


class Calendar(Base):
    __tablename__ = "academic_calendar"
    __table_args__ = (
        ForeignKeyConstraint(
            ["category_id"],
            ["academic_calendar_category.category_id"],
        ),
    )

    id_: Mapped[int] = mapped_column("academic_calendar_id", Integer, primary_key=True)
    category_id: Mapped[int] = mapped_column("category_id", Integer)
    title: Mapped[str] = mapped_column("title", String(100))
    description: Mapped[str] = mapped_column("description", String(1000))
    start_date: Mapped[datetime.date] = mapped_column("start_date", Date)
    end_date: Mapped[datetime.date] = mapped_column("end_date", Date)
    category: Mapped["CalendarCategory"] = relationship(
        "CalendarCategory",
        primaryjoin="Calendar.category_id == CalendarCategory.id_",
        viewonly=True,
        uselist=False,
    )


class CalendarVersion(Base):
    __tablename__ = "academic_calendar_version"

    id_: Mapped[int] = mapped_column("version_id", Integer, primary_key=True)
    name: Mapped[str] = mapped_column("version_name", String(30))
    created_at: Mapped[datetime.datetime] = mapped_column("created_at", DateTime)
