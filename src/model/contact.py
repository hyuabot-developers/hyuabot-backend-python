import datetime
from typing import List

from sqlalchemy import (
    Sequence,
    Integer,
    String,
    ForeignKeyConstraint,
    DateTime,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model import Base


class PhoneBookCategory(Base):
    __tablename__ = "phonebook_category"

    id_: Mapped[int] = mapped_column(
        "category_id",
        Integer,
        Sequence("phonebook_category_category_id_seq"),
        primary_key=True,
    )
    name: Mapped[str] = mapped_column("category_name", String(30))
    contacts: Mapped["List[PhoneBook]"] = relationship(
        "PhoneBook",
        cascade="all, delete-orphan",
        primaryjoin="PhoneBook.category_id == PhoneBookCategory.id_",
        viewonly=True,
        uselist=True,
    )


class PhoneBook(Base):
    __tablename__ = "phonebook"
    __table_args__ = (
        ForeignKeyConstraint(
            ["category_id"],
            ["phonebook_category.category_id"],
        ),
        ForeignKeyConstraint(
            ["campus_id"],
            ["campus.campus_id"],
        ),
    )

    id_: Mapped[int] = mapped_column("phonebook_id", Integer, primary_key=True)
    campus_id: Mapped[int] = mapped_column("campus_id", Integer)
    category_id: Mapped[int] = mapped_column("category_id", Integer)
    name: Mapped[str] = mapped_column("name", Text)
    phone: Mapped[str] = mapped_column("phone", String(30))
    category: Mapped["PhoneBookCategory"] = relationship(
        "PhoneBookCategory",
        primaryjoin="PhoneBook.category_id == PhoneBookCategory.id_",
        viewonly=True,
        uselist=False,
    )


class PhoneBookVersion(Base):
    __tablename__ = "phonebook_version"

    id_: Mapped[int] = mapped_column("version_id", Integer, primary_key=True)
    name: Mapped[str] = mapped_column("version_name", String(30))
    created_at: Mapped[datetime.datetime] = mapped_column(
        "created_at", DateTime(timezone=True),
    )
