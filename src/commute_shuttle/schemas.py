import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, Field


class CreateCommuteShuttleRouteRequest(BaseModel):
    name: Annotated[str, Field(max_length=15, alias="name")]
    route_description_korean: Annotated[str, Field(max_length=100, alias="korean")]
    route_description_english: Annotated[str, Field(max_length=100, alias="english")]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "서울캠퍼스",
                "korean": "서울캠퍼스 셔틀버스 노선",
                "english": "Seoul Campus Shuttle Bus Route",
            },
        }


class UpdateCommuteShuttleRouteRequest(BaseModel):
    route_description_korean: Annotated[
        Optional[str],
        Field(max_length=100, alias="korean"),
    ]
    route_description_english: Annotated[
        Optional[str],
        Field(max_length=100, alias="english"),
    ]

    class Config:
        json_schema_extra = {
            "example": {
                "korean": "서울캠퍼스 셔틀버스 노선",
                "english": "Seoul Campus Shuttle Bus Route",
            },
        }


class CreateCommuteShuttleStopRequest(BaseModel):
    name: Annotated[str, Field(max_length=50, alias="name")]
    description: Annotated[str, Field(max_length=100, alias="description")]
    latitude: Annotated[float, Field(alias="latitude")]
    longitude: Annotated[float, Field(alias="longitude")]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "서울캠퍼스",
                "description": "서울캠퍼스 셔틀버스 정류장",
                "latitude": 37.123456,
                "longitude": 127.123456,
            },
        }


class UpdateCommuteShuttleStopRequest(BaseModel):
    description: Annotated[Optional[str], Field(max_length=100, alias="description")]
    latitude: Annotated[Optional[float], Field(alias="latitude")]
    longitude: Annotated[Optional[float], Field(alias="longitude")]

    class Config:
        json_schema_extra = {
            "example": {
                "description": "서울캠퍼스 셔틀버스 정류장",
                "latitude": 37.123456,
                "longitude": 127.123456,
            },
        }


class CreateCommuteShuttleTimetableRequest(BaseModel):
    route_name: Annotated[str, Field(max_length=15, alias="route")]
    stop_name: Annotated[str, Field(max_length=50, alias="stop")]
    sequence: Annotated[int, Field(alias="sequence", ge=0)]
    departure_time: Annotated[datetime.time, Field(alias="time")]

    class Config:
        json_schema_extra = {
            "example": {
                "route": "서울캠퍼스",
                "stop": "서울캠퍼스",
                "sequence": 1,
                "time": "08:00",
            },
        }


class UpdateCommuteShuttleTimetableRequest(BaseModel):
    sequence: Annotated[Optional[int], Field(alias="sequence", ge=0)]
    departure_time: Annotated[Optional[datetime.time], Field(alias="time")]

    class Config:
        json_schema_extra = {
            "example": {
                "sequence": 1,
                "time": "08:00",
            },
        }


class CommuteShuttleRouteListItemResponse(BaseModel):
    route_name: Annotated[str, Field(max_length=15, alias="name")]
    route_description_korean: Annotated[str, Field(max_length=100, alias="korean")]
    route_description_english: Annotated[str, Field(max_length=100, alias="english")]


class CommuteShuttleRouteListResponse(BaseModel):
    data: Annotated[list["CommuteShuttleRouteListItemResponse"], Field(alias="data")]


class CommuteShuttleRouteDetailResponse(BaseModel):
    route_name: Annotated[str, Field(max_length=15, alias="name")]
    route_description_korean: Annotated[str, Field(max_length=100, alias="korean")]
    route_description_english: Annotated[str, Field(max_length=100, alias="english")]


class CommuteShuttleStopListItemResponse(BaseModel):
    stop_name: Annotated[str, Field(max_length=50, alias="name")]
    stop_description: Annotated[str, Field(max_length=100, alias="description")]
    latitude: Annotated[float, Field(alias="latitude")]
    longitude: Annotated[float, Field(alias="longitude")]


class CommuteShuttleStopListResponse(BaseModel):
    data: Annotated[list[CommuteShuttleStopListItemResponse], Field(alias="data")]


class CommuteShuttleStopDetailResponse(BaseModel):
    stop_name: Annotated[str, Field(max_length=50, alias="name")]
    stop_description: Annotated[str, Field(max_length=100, alias="description")]
    latitude: Annotated[float, Field(alias="latitude")]
    longitude: Annotated[float, Field(alias="longitude")]


class CommuteShuttleTimetableListItemResponse(BaseModel):
    route_name: Annotated[str, Field(max_length=15, alias="name")]
    stop_name: Annotated[str, Field(max_length=50, alias="stop")]
    sequence: Annotated[int, Field(alias="sequence", ge=0)]
    departure_time: Annotated[datetime.time, Field(alias="time")]


class CommuteShuttleTimetableListResponse(BaseModel):
    data: Annotated[
        list[CommuteShuttleTimetableListItemResponse],
        Field(alias="data"),
    ]


class CommuteShuttleTimetableDetailResponse(BaseModel):
    route_name: Annotated[str, Field(max_length=15, alias="name")]
    stop_name: Annotated[str, Field(max_length=50, alias="stop")]
    sequence: Annotated[int, Field(alias="sequence", ge=0)]
    departure_time: Annotated[datetime.time, Field(alias="time")]
