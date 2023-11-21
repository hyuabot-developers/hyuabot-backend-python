from typing import List

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model import Base
from model.notice import Notice


class User(Base):
    __tablename__ = "admin_user"

    id: Mapped[str] = mapped_column("user_id", String(20), primary_key=True)
    password: Mapped[str] = mapped_column("password", String(100))
    name: Mapped[str] = mapped_column("name", String(20))
    email: Mapped[str] = mapped_column("email", String(50))
    phone: Mapped[str] = mapped_column("phone", String(20))
    active: Mapped[bool] = mapped_column("active", Boolean, default=False)

    notices: Mapped["List[Notice]"] = relationship(
        "Notice",
        back_populates="user",
        cascade="all, delete-orphan",
    )
