import datetime
import uuid
from typing import Any

import pytz
from pydantic import UUID4
from sqlalchemy import insert, select, true, update

import utils
from database import (
    fetch_one,
    execute_query,
)
from model.user import User, RefreshToken
from user.config import auth_config
from user.exceptions import InvalidCredentials
from user.schemas import CreateUserRequest
from user.security import hash_password, verify_password


async def create_user(user: CreateUserRequest) -> dict[str, Any] | None:
    insert_query = (
        insert(User)
        .values(
            {
                "user_id": user.user_id,
                "password": hash_password(user.password),
                "name": user.name,
                "email": user.email,
                "phone": user.phone,
                "active": False,
            },
        )
        .returning(User)
    )

    return await fetch_one(insert_query)


async def get_user_by_id(user_id: str) -> dict[str, Any] | None:
    select_query = select(User).where(User.id == user_id)
    return await fetch_one(select_query)


async def get_active_user_by_id(user_id: str) -> dict[str, Any] | None:
    select_query = select(User).where(User.id == user_id, User.active == true())
    return await fetch_one(select_query)


async def create_refresh_token(
    *,
    user_id: str,
    refresh_token: str | None = None,
) -> str:
    if refresh_token is None:
        refresh_token = utils.generate_random_alphanum(64)

    insert_query = (
        insert(RefreshToken)
        .values(
            uuid=uuid.uuid4(),
            refresh_token=refresh_token,
            user_id=user_id,
            expired_at=(
                datetime.datetime.now(pytz.timezone("Asia/Seoul"))
                + datetime.timedelta(
                    seconds=auth_config.REFRESH_TOKEN_EXP,
                )
            ),
        )
        .returning(RefreshToken)
    )
    await execute_query(insert_query)

    return refresh_token


async def get_refresh_token(refresh_token: str) -> dict[str, Any] | None:
    select_query = select(RefreshToken).where(
        RefreshToken.refresh_token == refresh_token,
    )
    return await fetch_one(select_query)


async def expire_refresh_token(refresh_token_uuid: UUID4) -> None:
    update_query = (
        update(RefreshToken)
        .where(RefreshToken.uuid == refresh_token_uuid)
        .values(
            expired_at=datetime.datetime.now(pytz.timezone("Asia/Seoul"))
            - datetime.timedelta(days=1),
        )
    )
    await execute_query(update_query)


async def authenticate_user(
    username: str,
    password: str,
) -> dict[str, Any]:
    user = await get_active_user_by_id(user_id=username)
    if user is None:
        raise InvalidCredentials()

    if not verify_password(password, user["password"]):
        raise InvalidCredentials()

    return user
