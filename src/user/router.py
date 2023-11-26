from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, Response, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from exceptions import DetailedHTTPException
from user import service, utils, jwt
from user.dependancies import (
    create_valid_user,
    validate_refresh_token_user,
    validate_refresh_token,
)
from user.exceptions import InvalidCredentials
from user.jwt import parse_jwt_user_data
from user.schemas import UserDetailResponse, TokenResponse, CreateUserRequest

router = APIRouter()


@router.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
    response_model=UserDetailResponse,
)
async def register_user(
    new_user: CreateUserRequest = Depends(create_valid_user),
):
    user = await service.create_user(new_user)
    if user is None:
        raise DetailedHTTPException()
    return {
        "username": user["user_id"],
        "nickname": user["name"],
        "email": user["email"],
        "phone": user["phone"],
        "active": user["active"],
    }


@router.get(
    "/users/me",
    response_model=UserDetailResponse,
)
async def get_my_info(
    user_id: str = Depends(parse_jwt_user_data),
):
    user = await service.get_active_user_by_id(user_id)
    if user is None:
        raise InvalidCredentials()
    return {
        "username": user["user_id"],
        "nickname": user["name"],
        "email": user["email"],
        "phone": user["phone"],
        "active": user["active"],
    }


@router.post(
    "/users/token",
    response_model=TokenResponse,
)
async def auth_user(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = await service.authenticate_user(form_data.username, form_data.password)
    refresh_token = await service.create_refresh_token(user_id=user["user_id"])
    response.set_cookie(
        **utils.get_refresh_token_settings(refresh_token),
    )
    return {
        "access_token": jwt.create_access_token(user=user),
        "refresh_token": refresh_token,
    }


@router.put(
    "/users/token",
    response_model=TokenResponse,
)
async def refresh_tokens(
    worker: BackgroundTasks,
    response: Response,
    refresh_token: dict[str, Any] = Depends(validate_refresh_token),
    user: dict[str, Any] = Depends(validate_refresh_token_user),
):
    refresh_token_value = await service.create_refresh_token(
        user_id=str(user["user_id"]),
    )
    response.set_cookie(
        **utils.get_refresh_token_settings(refresh_token_value),
    )
    worker.add_task(service.expire_refresh_token, UUID(refresh_token["uuid"]))
    return {
        "access_token": jwt.create_access_token(user=user),
        "refresh_token": refresh_token_value,
    }


@router.delete("/users/token")
async def logout(
    response: Response,
    refresh_token: dict[str, Any] = Depends(validate_refresh_token),
):
    await service.expire_refresh_token(refresh_token["uuid"])
    response.delete_cookie(
        **utils.get_refresh_token_settings(
            refresh_token["refresh_token"],
            expired=True,
        ),
    )
