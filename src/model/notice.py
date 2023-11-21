import datetime
from typing import List

from sqlalchemy import String, DateTime, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship

from model import Base
from model.user import User


class NoticeCategory(Base):
    __tablename__ = "notice_category"

    id: Mapped[int] = mapped_column("category_id", Integer, primary_key=True)
    name: Mapped[str] = mapped_column("category_name", String(20))

    notices: Mapped["List[Notice]"] = relationship(
        "Notice",
        back_populates="category",
        cascade="all, delete-orphan",
    )


class Notice(Base):
    __tablename__ = "notice"

    id: Mapped[int] = mapped_column("notice_id", Integer, primary_key=True)
    category_id: Mapped[int] = mapped_column("category_id", Integer)
    user_id: Mapped[str] = mapped_column("user_id", String(20))
    title: Mapped[str] = mapped_column("title", String(100))
    url: Mapped[str] = mapped_column("url", String(200))
    expired_at: Mapped[datetime.datetime] = mapped_column("expired_at", DateTime)

    category: Mapped["NoticeCategory"] = relationship(
        "NoticeCategory",
        back_populates="notices",
    )
    user: Mapped["User"] = relationship(
        "User",
        back_populates="notices",
    )
