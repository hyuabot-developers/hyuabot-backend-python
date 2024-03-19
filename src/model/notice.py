import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, Integer, String, ForeignKeyConstraint, Sequence
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model import Base

if TYPE_CHECKING:
    from model.user import User


class NoticeCategory(Base):
    __tablename__ = "notice_category"

    id_: Mapped[int] = mapped_column(
        "category_id",
        Integer,
        Sequence("notice_category_category_id_seq"),
        primary_key=True,
    )
    name: Mapped[str] = mapped_column("category_name", String(20))

    notices: Mapped["List[Notice]"] = relationship(
        "Notice",
        back_populates="category",
        cascade="all, delete-orphan",
        primaryjoin="Notice.category_id == NoticeCategory.id_",
        viewonly=True,
    )


class Notice(Base):
    __tablename__ = "notices"
    __table_args__ = (
        ForeignKeyConstraint(
            ["category_id"],
            ["notice_category.category_id"],
        ),
        ForeignKeyConstraint(
            ["user_id"],
            ["admin_user.user_id"],
        ),
    )

    id_: Mapped[int] = mapped_column("notice_id", Integer, primary_key=True)
    category_id: Mapped[int] = mapped_column("category_id", Integer)
    user_id: Mapped[str] = mapped_column("user_id", String(20))
    title: Mapped[str] = mapped_column("title", String(100))
    url: Mapped[str] = mapped_column("url", String(200))
    language: Mapped[str] = mapped_column(
        "language",
        String(10),
        default="korean",
    )
    expired_at: Mapped[datetime.datetime] = mapped_column(
        "expired_at",
        DateTime(timezone=True),
    )

    category: Mapped["NoticeCategory"] = relationship(
        "NoticeCategory",
        back_populates="notices",
    )
    user: Mapped["User"] = relationship(
        "User",
        back_populates="notices",
        primaryjoin="Notice.user_id == User.id_",
    )
