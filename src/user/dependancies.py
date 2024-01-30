import datetime

import pytz
from fastapi import Cookie, Depends

from model.user import RefreshToken, User
from user import service
from user.exceptions import EmailAlreadyExists, InvalidRefreshToken
from user.schemas import CreateUserRequest


async def create_valid_user(new_user: CreateUserRequest) -> CreateUserRequest:
    if await service.get_user_by_id(new_user.user_id):
        raise EmailAlreadyExists()

    return new_user


async def validate_refresh_token(
    refresh_token: str = Cookie(..., alias="refresh_token"),
) -> RefreshToken:
    saved_refresh_token = await service.get_refresh_token(refresh_token)
    if saved_refresh_token is None:
        raise InvalidRefreshToken()

    if not _validate_refresh_token_user(saved_refresh_token):
        raise InvalidRefreshToken()

    return saved_refresh_token


async def validate_refresh_token_user(
    refresh_token: RefreshToken = Depends(validate_refresh_token),
) -> User:
    user = await service.get_active_user_by_id(refresh_token.user_id)
    if user is None:
        raise InvalidRefreshToken()

    return user


def _validate_refresh_token_user(refresh_token: RefreshToken) -> bool:
    return datetime.datetime.now(pytz.timezone("Asia/Seoul")) < refresh_token.expired_at
