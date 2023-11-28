from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from typing_extensions import Annotated


class CreateUserRequest(BaseModel):
    user_id: Annotated[str, Field(max_length=20, alias="username")]
    name: Annotated[str, Field(max_length=20, alias="nickname")]
    email: Annotated[EmailStr, Field(examples=["test@email.com"])]
    password: Annotated[str, Field(examples=["password"])]
    phone: Annotated[str, Field(max_length=20, alias="phone")]

    class Config:
        json_schema_extra = {
            "example": {
                "username": "test",
                "nickname": "test",
                "email": "test@email.com",
                "password": "password",
                "phone": "01012345678",
            },
        }


class LoginUserRequest(BaseModel):
    user_id: Annotated[str, Field(max_length=20, alias="username")]
    password: Annotated[str, Field(examples=["password"])]

    class Config:
        json_schema_extra = {
            "example": {
                "username": "test",
                "password": "password",
            },
        }


class UpdateUserRequest(BaseModel):
    email: Annotated[Optional[EmailStr], Field(examples=["test@email.com"])]
    password: Annotated[Optional[str], Field(examples=["password"])]
    phone_number: Annotated[Optional[str], Field(max_length=20, alias="phoneNumber")]
    active: Annotated[Optional[bool], Field(default=False)]

    class Config:
        json_schema_extra = {
            "example": {
                "email": "test@email.com",
                "password": "password",
                "phoneNumber": "01012345678",
                "active": False,
            },
        }


class UserListResponse(BaseModel):
    data: Annotated[list["UserListItemResponse"], Field(alias="data")]


class UserListItemResponse(BaseModel):
    user_id: Annotated[str, Field(max_length=20, alias="id")]
    email: Annotated[EmailStr, Field(alias="email")]


class UserDetailResponse(BaseModel):
    user_id: Annotated[str, Field(max_length=20, alias="username")]
    name: Annotated[str, Field(max_length=20, alias="nickname")]
    email: Annotated[EmailStr, Field(alias="email")]
    phone_number: Annotated[str, Field(max_length=20, alias="phone")]
    active: Annotated[bool, Field(default=False)]


class TokenResponse(BaseModel):
    access_token: Annotated[str, Field(alias="access_token")]
    refresh_token: Annotated[str, Field(alias="refresh_token")]
