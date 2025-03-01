import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, Field


class CreateShuttleHolidayRequest(BaseModel):
    date: Annotated[datetime.date, Field(alias="date")]
    type_: Annotated[str, Field(alias="type", pattern=r"^(weekends|halt)$")]
    calendar: Annotated[str, Field(alias="calendar", pattern=r"^(lunar|solar)$")]

    class Config:
        json_schema_extra = {
            "example": {
                "date": "2021-07-31",
                "type": "weekends",
                "calendar": "lunar",
            },
        }


class CreateShuttlePeriodTypeRequest(BaseModel):
    type_: Annotated[str, Field(alias="type", max_length=20)]

    class Config:
        json_schema_extra = {
            "example": {
                "type": "weekday",
            },
        }


class CreateShuttlePeriodRequest(BaseModel):
    type_: Annotated[str, Field(alias="type", max_length=20)]
    start: Annotated[datetime.date, Field(alias="start")]
    end: Annotated[datetime.date, Field(alias="end")]

    class Config:
        json_schema_extra = {
            "example": {
                "type": "semester",
                "start": "2021-07-31",
                "end": "2021-08-31",
            },
        }


class CreateShuttleRouteRequest(BaseModel):
    name: Annotated[str, Field(max_length=15, alias="name")]
    tag: Annotated[str, Field(max_length=10, alias="tag")]
    route_description_korean: Annotated[str, Field(max_length=100, alias="korean")]
    route_description_english: Annotated[str, Field(max_length=100, alias="english")]
    start_stop_id: Annotated[str, Field(alias="start", max_length=15)]
    end_stop_id: Annotated[str, Field(alias="end", max_length=15)]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "DHSS",
                "tag": "DH",
                "korean": "셔틀콕 ~ 한대앞 ~ 셔틀콕",
                "english": "Shuttlecock ~ Station ~ Shuttlecock",
                "start": "shuttlecock_o",
                "end": "shuttlecock_i",
            },
        }


class UpdateShuttleRouteRequest(BaseModel):
    tag: Annotated[Optional[str], Field(max_length=10, alias="tag")]
    route_description_korean: Annotated[
        Optional[str],
        Field(max_length=100, alias="korean"),
    ]
    route_description_english: Annotated[
        Optional[str],
        Field(max_length=100, alias="english"),
    ]
    start_stop_id: Annotated[Optional[str], Field(alias="start", max_length=15)]
    end_stop_id: Annotated[Optional[str], Field(alias="end", max_length=15)]

    class Config:
        json_schema_extra = {
            "example": {
                "tag": "DH",
                "korean": "셔틀콕 ~ 한대앞 ~ 셔틀콕",
                "english": "Shuttlecock ~ Station ~ Shuttlecock",
                "start": "shuttlecock_o",
                "end": "shuttlecock_i",
            },
        }


class CreateShuttleStopRequest(BaseModel):
    name: Annotated[str, Field(max_length=15, alias="name")]
    latitude: Annotated[float, Field(alias="latitude")]
    longitude: Annotated[float, Field(alias="longitude")]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "shuttlecock_o",
                "latitude": 37.123456,
                "longitude": 127.123456,
            },
        }


class UpdateShuttleStopRequest(BaseModel):
    latitude: Annotated[Optional[float], Field(alias="latitude")]
    longitude: Annotated[Optional[float], Field(alias="longitude")]

    class Config:
        json_schema_extra = {
            "example": {
                "latitude": 37.123456,
                "longitude": 127.123456,
            },
        }


class CreateShuttleRouteStopRequest(BaseModel):
    stop_name: Annotated[str, Field(max_length=15, alias="stop")]
    sequence: Annotated[int, Field(alias="sequence", ge=0)]
    cumulative_time: Annotated[int, Field(alias="cumulativeTime")]

    class Config:
        json_schema_extra = {
            "example": {
                "stop": "shuttlecock_o",
                "sequence": 1,
                "cumulativeTime": 300,
            },
        }


class UpdateShuttleRouteStopRequest(BaseModel):
    sequence: Annotated[Optional[int], Field(alias="sequence", ge=0)]
    cumulative_time: Annotated[Optional[int], Field(alias="cumulativeTime")]

    class Config:
        json_schema_extra = {
            "example": {
                "sequence": 1,
                "cumulativeTime": 300,
            },
        }


class CreateShuttleTimetableRequest(BaseModel):
    period_type: Annotated[str, Field(alias="period", max_length=20)]
    is_weekdays: Annotated[bool, Field(alias="weekdays")]
    route_name: Annotated[str, Field(max_length=15, alias="route")]
    departure_time: Annotated[datetime.time, Field(alias="time")]

    class Config:
        json_schema_extra = {
            "example": {
                "period": "weekday",
                "weekdays": True,
                "route": "DHSS",
                "time": "08:00",
            },
        }


class UpdateShuttleTimetableRequest(BaseModel):
    period_type: Annotated[Optional[str], Field(alias="period", max_length=20)]
    is_weekdays: Annotated[Optional[bool], Field(alias="weekdays")]
    route_name: Annotated[Optional[str], Field(max_length=15, alias="route")]
    departure_time: Annotated[Optional[datetime.time], Field(alias="time")]

    class Config:
        json_schema_extra = {
            "example": {
                "period": "weekday",
                "weekdays": True,
                "route": "DHSS",
                "time": "08:00",
            },
        }


class ShuttleHolidayItemResponse(BaseModel):
    date: Annotated[datetime.date, Field(alias="date")]
    type_: Annotated[str, Field(alias="type", pattern=r"^(weekends|halt)$")]
    calendar: Annotated[str, Field(alias="calendar", pattern=r"^(lunar|solar)$")]


class ShuttleHolidayListResponse(BaseModel):
    data: Annotated[list["ShuttleHolidayItemResponse"], Field(alias="data")]


class ShuttlePeriodItemResponse(BaseModel):
    type_: Annotated[str, Field(alias="type", max_length=20)]
    start: Annotated[datetime.datetime, Field(alias="start")]
    end: Annotated[datetime.datetime, Field(alias="end")]


class ShuttlePeriodListResponse(BaseModel):
    data: Annotated[list["ShuttlePeriodItemResponse"], Field(alias="data")]


class ShuttleRouteDetailResponse(BaseModel):
    name: Annotated[str, Field(max_length=15, alias="name")]
    tag: Annotated[str, Field(max_length=10, alias="tag")]
    route_description_korean: Annotated[str, Field(max_length=100, alias="korean")]
    route_description_english: Annotated[str, Field(max_length=100, alias="english")]
    start_stop_id: Annotated[str, Field(alias="start", max_length=15)]
    end_stop_id: Annotated[str, Field(alias="end", max_length=15)]


class ShuttleRouteListResponse(BaseModel):
    data: Annotated[list["ShuttleRouteDetailResponse"], Field(alias="data")]


class ShuttleRouteStopResponse(BaseModel):
    stop_name: Annotated[str, Field(max_length=15, alias="stop")]
    sequence: Annotated[int, Field(alias="sequence", ge=0)]
    cumulative_time: Annotated[datetime.timedelta, Field(alias="cumulativeTime")]


class ShuttleStopItemResponse(BaseModel):
    name: Annotated[str, Field(max_length=15, alias="name")]
    latitude: Annotated[float, Field(alias="latitude")]
    longitude: Annotated[float, Field(alias="longitude")]


class ShuttleStopListResponse(BaseModel):
    data: Annotated[list["ShuttleStopItemResponse"], Field(alias="data")]


class ShuttleRouteStopItemResponse(BaseModel):
    route_name: Annotated[str, Field(max_length=15, alias="route")]
    stop_name: Annotated[str, Field(max_length=15, alias="stop")]
    sequence: Annotated[int, Field(alias="sequence", ge=0)]
    cumulative_time: Annotated[int, Field(alias="cumulativeTime")]


class ShuttleRouteStopListResponse(BaseModel):
    data: Annotated[list["ShuttleRouteStopItemResponse"], Field(alias="data")]


class ShuttleTimetableItemResponse(BaseModel):
    sequence: Annotated[int, Field(alias="sequence", ge=1)]
    route_name: Annotated[str, Field(max_length=15, alias="route")]
    period_type: Annotated[str, Field(alias="period", max_length=20)]
    is_weekdays: Annotated[bool, Field(alias="weekdays")]
    departure_time: Annotated[datetime.time, Field(alias="time")]


class ShuttleTimetableListResponse(BaseModel):
    data: Annotated[list["ShuttleTimetableItemResponse"], Field(alias="data")]


class ShuttleTimetableViewItemResponse(BaseModel):
    sequence: Annotated[int, Field(alias="sequence", ge=1)]
    route_name: Annotated[str, Field(max_length=15, alias="route")]
    stop_name: Annotated[str, Field(max_length=15, alias="stop")]
    period_type: Annotated[str, Field(alias="period", max_length=20)]
    is_weekdays: Annotated[bool, Field(alias="weekdays")]
    departure_time: Annotated[datetime.time, Field(alias="time")]


class ShuttleTimetableViewResponse(BaseModel):
    data: Annotated[list["ShuttleTimetableViewItemResponse"], Field(alias="data")]
