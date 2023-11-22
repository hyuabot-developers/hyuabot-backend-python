from typing import Optional

from pydantic import BaseModel, Field, EmailStr, SecretStr
from typing_extensions import Annotated


class CreateUserRequest(BaseModel):
    user_id: Annotated[str, Field(max_length=20, alias="userID")]
    email: Annotated[EmailStr, Field(examples=["test@email.com"])]
    password: Annotated[SecretStr, Field(examples=["password"])]
    phone_number: Annotated[str, Field(max_length=20, alias="phoneNumber")]

    class Config:
        schema_extra = {
            "example": {
                "userID": "test",
                "email": "test@email.com",
                "password": "password",
                "phoneNumber": "01012345678",
            }
        }


class LoginUserRequest(BaseModel):
    user_id: Annotated[str, Field(max_length=20, alias="userID")]
    password: Annotated[SecretStr, Field(examples=["password"])]

    class Config:
        schema_extra = {
            "example": {
                "userID": "test",
                "password": "password",
            }
        }


class UpdateUserRequest(BaseModel):
    email: Annotated[Optional[EmailStr], Field(examples=["test@email.com"])]
    password: Annotated[Optional[SecretStr], Field(examples=["password"])]
    phone_number: Annotated[Optional[str], Field(max_length=20, alias="phoneNumber")]
    active: Annotated[Optional[bool], Field(default=False)]

    class Config:
        schema_extra = {
            "example": {
                "email": "test@email.com",
                "password": "password",
                "phoneNumber": "01012345678",
                "active": False,
            }
        }
