import datetime
from typing import TYPE_CHECKING

import pytz
from sqlalchemy import Boolean, String, DateTime, UUID
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import Mapped, mapped_column

from model import Base

if TYPE_CHECKING:
    pass


class User(Base):
    __tablename__ = "admin_user"

    id: Mapped[str] = mapped_column("user_id", String(20), primary_key=True)
    password: Mapped[bytes] = mapped_column("password", BYTEA)
    name: Mapped[str] = mapped_column("name", String(20))
    email: Mapped[str] = mapped_column("email", String(50))
    phone: Mapped[str] = mapped_column("phone", String(20))
    active: Mapped[bool] = mapped_column("active", Boolean, default=False)


class RefreshToken(Base):
    __tablename__ = "auth_refresh_token"

    uuid: Mapped[str] = mapped_column("uuid", UUID, primary_key=True)
    user_id: Mapped[str] = mapped_column("user_id", String(20))
    refresh_token: Mapped[str] = mapped_column("refresh_token", String(64))
    expired_at: Mapped[datetime.datetime] = mapped_column(
        "expired_at",
        DateTime(timezone=True),
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        "created_at",
        DateTime(timezone=True),
        default=datetime.datetime.now(pytz.timezone("Asia/Seoul")),
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        "updated_at",
        DateTime(timezone=True),
        default=datetime.datetime.now(pytz.timezone("Asia/Seoul")),
    )
