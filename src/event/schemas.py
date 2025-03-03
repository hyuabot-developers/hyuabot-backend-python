import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, Field


class CreateCalendarCategoryRequest(BaseModel):
    name: Annotated[str, Field(max_length=20, alias="name")]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "전체",
            },
        }


class CreateCalendarReqeust(BaseModel):
    title: Annotated[str, Field(max_length=100, alias="title")]
    description: Annotated[str, Field(max_length=1000, alias="description")]
    start_date: Annotated[datetime.date, Field(alias="start")]
    end_date: Annotated[datetime.date, Field(alias="end")]

    class Config:
        json_schema_extra = {
            "example": {
                "title": "일정",
                "description": "일정입니다.",
                "start": "2021-07-01",
                "end": "2021-07-31",
            },
        }


class UpdateCalendarRequest(BaseModel):
    title: Annotated[
        Optional[str],
        Field(max_length=100, alias="title", default=None),
    ]
    description: Annotated[
        Optional[str],
        Field(max_length=1000, alias="description", default=None),
    ]
    start_date: Annotated[
        Optional[datetime.date],
        Field(alias="start", default=None),
    ]
    end_date: Annotated[
        Optional[datetime.date],
        Field(alias="end", default=None),
    ]

    class Config:
        json_schema_extra = {
            "example": {
                "title": "일정",
                "description": "일정입니다.",
                "start": "2021-07-01",
                "end": "2021-07-31",
            },
        }


class CalendarCategoryDetailResponse(BaseModel):
    id_: Annotated[int, Field(alias="id", ge=1)]
    name: Annotated[str, Field(max_length=20, alias="name")]


class CalendarCategoryListResponse(BaseModel):
    data: Annotated[list[CalendarCategoryDetailResponse], Field(alias="data")]


class CalendarDetailResponse(BaseModel):
    id_: Annotated[int, Field(alias="id", ge=1)]
    title: Annotated[str, Field(max_length=100, alias="title")]
    description: Annotated[str, Field(max_length=1000, alias="description")]
    start_date: Annotated[datetime.date, Field(alias="start")]
    end_date: Annotated[datetime.date, Field(alias="end")]


class CalendarListResponse(BaseModel):
    data: Annotated[list[CalendarDetailResponse], Field(alias="data")]
