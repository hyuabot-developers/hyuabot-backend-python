import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, Field


class CreateShuttleHolidayRequest(BaseModel):
    date: Annotated[
        datetime.date,
        Field(alias="date", regex=r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
    ]
    type: Annotated[str, Field(alias="type", regex=r"^(weekends|halt)$")]
    calendar: Annotated[str, Field(alias="calendar", regex=r"^(lunar|solar)$")]

    class Config:
        schema_extra = {
            "example": {
                "date": "2021-07-31",
                "type": "weekends",
                "calendar": "lunar",
            },
        }


class CreateShuttlePeriodTypeRequest(BaseModel):
    type: Annotated[str, Field(alias="type", max_length=20)]

    class Config:
        schema_extra = {
            "example": {
                "type": "weekday",
            },
        }


class CreateShuttlePeriodRequest(BaseModel):
    type: Annotated[str, Field(alias="type", max_length=20)]
    start: Annotated[
        datetime.datetime,
        Field(
            alias="start",
            regex=r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}+09:00$",
        ),
    ]
    end: Annotated[
        datetime.datetime,
        Field(
            alias="end",
            regex=r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}+09:00$",
        ),
    ]

    class Config:
        schema_extra = {
            "example": {
                "type": "weekday",
                "start": "2021-07-31T00:00:00+09:00",
                "end": "2021-07-31T00:00:00+09:00",
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
        schema_extra = {
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
        schema_extra = {
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
        schema_extra = {
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
        schema_extra = {
            "example": {
                "latitude": 37.123456,
                "longitude": 127.123456,
            },
        }


class CreateShuttleRouteStopRequest(BaseModel):
    route_name: Annotated[str, Field(max_length=15, alias="route")]
    stop_name: Annotated[str, Field(max_length=15, alias="stop")]
    sequence: Annotated[int, Field(alias="sequence", ge=1)]
    cumulative_time: Annotated[
        datetime.timedelta,
        Field(alias="cumulativeTime", regex=r"^[0-9]{2}:[0-9]{2}:[0-9]{2}$"),
    ]

    class Config:
        schema_extra = {
            "example": {
                "route": "DHSS",
                "stop": "shuttlecock_o",
                "sequence": 1,
                "cumulativeTime": "00:00:00",
            },
        }


class UpdateShuttleRouteStopRequest(BaseModel):
    sequence: Annotated[Optional[int], Field(alias="sequence", ge=1)]
    cumulative_time: Annotated[
        Optional[datetime.timedelta],
        Field(alias="cumulativeTime", regex=r"^[0-9]{2}:[0-9]{2}:[0-9]{2}$"),
    ]

    class Config:
        schema_extra = {
            "example": {
                "sequence": 1,
                "cumulativeTime": "00:00:00",
            },
        }


class CreateShuttleTimetableRequest(BaseModel):
    period_type: Annotated[str, Field(alias="period", max_length=20)]
    is_weekdays: Annotated[bool, Field(alias="weekdays")]
    route_name: Annotated[str, Field(max_length=15, alias="route")]
    departure_time: Annotated[
        datetime.time,
        Field(alias="departureTime", regex=r"^[0-9]{2}:[0-9]{2}$"),
    ]

    class Config:
        schema_extra = {
            "example": {
                "period": "weekday",
                "weekdays": True,
                "route": "DHSS",
                "departureTime": "08:00",
            },
        }


class UpdateShuttleTimetableRequest(BaseModel):
    period_type: Annotated[Optional[str], Field(alias="period", max_length=20)]
    is_weekdays: Annotated[Optional[bool], Field(alias="weekdays")]
    route_name: Annotated[Optional[str], Field(max_length=15, alias="route")]
    departure_time: Annotated[
        Optional[datetime.time],
        Field(alias="departureTime", regex=r"^[0-9]{2}:[0-9]{2}$"),
    ]

    class Config:
        schema_extra = {
            "example": {
                "period": "weekday",
                "weekdays": True,
                "route": "DHSS",
                "departureTime": "08:00",
            },
        }
