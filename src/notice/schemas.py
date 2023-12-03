import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, Field


class CreateNoticeCategoryRequest(BaseModel):
    name: Annotated[str, Field(max_length=20, alias="name")]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "공지사항",
            },
        }


class CreateNoticeReqeust(BaseModel):
    title: Annotated[str, Field(max_length=100, alias="title")]
    url: Annotated[str, Field(max_length=100, alias="url")]
    expired_at: Annotated[
        Optional[datetime.datetime],
        Field(alias="expired", default=None),
    ]

    class Config:
        json_schema_extra = {
            "example": {
                "title": "공지사항",
                "url": "https://www.google.com",
                "expired": "2021-07-31T00:00:00+09:00",
            },
        }


class UpdateNoticeRequest(BaseModel):
    title: Annotated[
        Optional[str],
        Field(max_length=100, alias="title", default=None),
    ]
    url: Annotated[
        Optional[str],
        Field(max_length=100, alias="url", default=None),
    ]
    expired_at: Annotated[
        Optional[datetime.datetime],
        Field(alias="expired", default=None),
    ]

    class Config:
        json_schema_extra = {
            "example": {
                "title": "공지사항",
                "url": "https://www.google.com",
                "expired": "2021-07-31T00:00:00+09:00",
            },
        }


class NoticeCategoryListItemResponse(BaseModel):
    id: Annotated[int, Field(alias="id", ge=1)]
    name: Annotated[str, Field(max_length=20, alias="name")]


class NoticeCategoryListResponse(BaseModel):
    data: Annotated[list[NoticeCategoryListItemResponse], Field(alias="data")]


class NoticeCategoryDetailResponse(BaseModel):
    id: Annotated[int, Field(alias="id", ge=1)]
    name: Annotated[str, Field(max_length=20, alias="name")]


class NoticeListItemResponse(BaseModel):
    id: Annotated[int, Field(alias="id", ge=1)]
    title: Annotated[str, Field(max_length=100, alias="title")]
    url: Annotated[str, Field(max_length=100, alias="url")]
    user_id: Annotated[str, Field(alias="userID")]
    expired_at: Annotated[
        Optional[datetime.datetime],
        Field(alias="expiredAt"),
    ]


class NoticeListResponse(BaseModel):
    data: Annotated[list[NoticeListItemResponse], Field(alias="data")]


class NoticeDetailResponse(BaseModel):
    id: Annotated[int, Field(alias="id", ge=1)]
    title: Annotated[str, Field(max_length=100, alias="title")]
    url: Annotated[str, Field(max_length=100, alias="url")]
    user_id: Annotated[str, Field(alias="userID")]
    expired_at: Annotated[
        Optional[datetime.datetime],
        Field(alias="expiredAt"),
    ]
