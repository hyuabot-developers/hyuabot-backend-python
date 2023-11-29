import datetime
from typing import Optional

from pydantic import BaseModel, Field
from typing_extensions import Annotated


class CreateSubwayStation(BaseModel):
    name: Annotated[str, Field(max_length=30, alias="name")]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "서울역",
            },
        }


class CreateSubwayRoute(BaseModel):
    id: Annotated[int, Field(alias="id", ge=1)]
    name: Annotated[str, Field(max_length=30, alias="name")]

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1001,
                "name": "1호선",
            },
        }


class UpdateSubwayRoute(BaseModel):
    name: Annotated[Optional[str], Field(max_length=30, alias="name")]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "1호선",
            },
        }


class CreateSubwayRouteStation(BaseModel):
    id: Annotated[str, Field(alias="id", pattern=r"^K[0-9]{3}$")]
    name: Annotated[str, Field(max_length=30, alias="name")]
    route_id: Annotated[int, Field(alias="routeID", ge=1)]
    sequence: Annotated[int, Field(alias="sequence", ge=0)]
    cumulative_time: Annotated[datetime.timedelta, Field(alias="cumulativeTime")]

    class Config:
        json_schema_extra = {
            "example": {
                "id": "K101",
                "name": "서울역",
                "routeID": 1001,
                "sequence": 1,
                "cumulativeTime": "00:00:00",
            },
        }


class UpdateSubwayRouteStation(BaseModel):
    name: Annotated[Optional[str], Field(max_length=30, alias="name")]
    sequence: Annotated[Optional[int], Field(alias="sequence", ge=0)]
    cumulative_time: Annotated[datetime.timedelta, Field(alias="cumulativeTime")]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "서울역",
                "sequence": 1,
                "cumulativeTime": "00:00:00",
            },
        }


class CreateSubwayTimetable(BaseModel):
    start_station_id: Annotated[
        str,
        Field(alias="startStationID", pattern=r"^K[0-9]{3}$"),
    ]
    terminal_station_id: Annotated[
        str,
        Field(alias="terminalStationID", pattern=r"^K[0-9]{3}$"),
    ]
    departure_time: Annotated[datetime.time, Field(alias="departureTime")]
    weekday: Annotated[str, Field(alias="weekday", max_length=10)]
    heading: Annotated[str, Field(alias="heading", max_length=10)]

    class Config:
        json_schema_extra = {
            "example": {
                "startStationID": "K101",
                "terminalStationID": "K101",
                "departureTime": "00:00:00",
                "weekday": "weekday",
                "heading": "up",
            },
        }


class SubwayRouteItemResponse(BaseModel):
    id: Annotated[int, Field(alias="id", ge=1)]
    name: Annotated[str, Field(max_length=30, alias="name")]


class SubwayStationItemResponse(BaseModel):
    name: Annotated[str, Field(max_length=30, alias="name")]


class SubwayRouteListResponse(BaseModel):
    data: Annotated[list[SubwayRouteItemResponse], Field(alias="data")]


class SubwayStationListResponse(BaseModel):
    data: Annotated[list[SubwayStationItemResponse], Field(alias="data")]


class SubwayRouteStationListItemResponse(BaseModel):
    id: Annotated[str, Field(alias="id", pattern=r"^K[0-9]{3}$")]
    name: Annotated[str, Field(max_length=30, alias="name")]
    route_id: Annotated[int, Field(alias="routeID", ge=1)]
    sequence: Annotated[int, Field(alias="sequence", ge=0)]
    cumulative_time: Annotated[
        str,
        Field(alias="cumulativeTime", pattern=r"^[0-9]{2}:[0-9]{2}:[0-9]{2}$"),
    ]


class SubwayRouteStationListResponse(BaseModel):
    data: Annotated[list[SubwayRouteStationListItemResponse], Field(alias="data")]


class SubwayRouteStationDetailResponse(BaseModel):
    id: Annotated[str, Field(alias="id", pattern=r"^K[0-9]{3}$")]
    name: Annotated[str, Field(max_length=30, alias="name")]
    route_id: Annotated[int, Field(alias="routeID", ge=1)]
    sequence: Annotated[int, Field(alias="sequence", ge=0)]
    cumulative_time: Annotated[
        str,
        Field(alias="cumulativeTime", pattern=r"^[0-9]{2}:[0-9]{2}:[0-9]{2}$"),
    ]


class SubwayStartEndStation(BaseModel):
    id: Annotated[str, Field(alias="id", pattern=r"^K[0-9]{3}$")]
    name: Annotated[str, Field(max_length=30, alias="name")]


class SubwayTimetableItemResponse(BaseModel):
    station_id: Annotated[str, Field(alias="stationID", pattern=r"^K[0-9]{3}$")]
    start_station_id: Annotated[str, Field(alias="start_station_id")]
    terminal_station_id: Annotated[str, Field(alias="terminal_station_id")]
    departure_time: Annotated[datetime.time, Field(alias="departureTime")]
    weekday: Annotated[str, Field(alias="weekday", max_length=10)]
    heading: Annotated[str, Field(alias="heading", max_length=10)]


class SubwayTimetableListResponse(BaseModel):
    data: Annotated[list[SubwayTimetableItemResponse], Field(alias="data")]


class SubwayRealtimeItemResponse(BaseModel):
    station_id: Annotated[str, Field(alias="stationID", pattern=r"^K[0-9]{3}$")]
    sequence: Annotated[int, Field(alias="sequence", ge=0)]
    current_station: Annotated[str, Field(alias="current")]
    remaining_stations: Annotated[int, Field(alias="station", ge=0)]
    remaining_time: Annotated[
        str,
        Field(alias="time", pattern=r"^[0-9]{2}:[0-9]{2}:[0-9]{2}$"),
    ]
    heading: Annotated[str, Field(alias="heading", max_length=10)]
    train_number: Annotated[str, Field(alias="trainNumber", max_length=10)]
    is_express: Annotated[bool, Field(alias="express")]
    is_last: Annotated[bool, Field(alias="last")]
    terminal_station_id: Annotated[str, Field(alias="terminalStationID")]
    status: Annotated[int, Field(alias="status")]


class SubwayRealtimeListResponse(BaseModel):
    data: Annotated[list[SubwayRealtimeItemResponse], Field(alias="data")]
