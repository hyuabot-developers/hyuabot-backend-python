from typing import Optional

from pydantic import BaseModel, Field
from typing_extensions import Annotated


class CreateSubwayStation(BaseModel):
    name: Annotated[str, Field(max_length=30, alias="name")]

    class Config:
        schema_extra = {
            "example": {
                "name": "서울역",
            }
        }


class CreateSubwayRoute(BaseModel):
    id: Annotated[int, Field(alias="id", ge=1)]
    name: Annotated[str, Field(max_length=30, alias="name")]

    class Config:
        schema_extra = {
            "example": {
                "id": 1001,
                "name": "1호선",
            }
        }


class UpdateSubwayRoute(BaseModel):
    name: Annotated[Optional[str], Field(max_length=30, alias="name")]

    class Config:
        schema_extra = {
            "example": {
                "name": "1호선",
            }
        }


class CreateSubwayRouteStation(BaseModel):
    id: Annotated[str, Field(alias="id", pattern=r"^K[0-9]{3}$")]
    name: Annotated[str, Field(max_length=30, alias="name")]
    route_id: Annotated[int, Field(alias="routeID", ge=1)]
    sequence: Annotated[int, Field(alias="sequence", ge=1)]
    cumulative_time: Annotated[str, Field(alias="cumulativeTime", regex=r"^[0-9]{2}:[0-9]{2}:[0-9]{2}$")]

    class Config:
        schema_extra = {
            "example": {
                "id": "K101",
                "name": "서울역",
                "routeID": 1001,
                "sequence": 1,
                "cumulativeTime": "00:00:00",
            }
        }


class UpdateSubwayRouteStation(BaseModel):
    name: Annotated[Optional[str], Field(max_length=30, alias="name")]
    sequence: Annotated[Optional[int], Field(alias="sequence", ge=1)]
    cumulative_time: Annotated[Optional[str], Field(alias="cumulativeTime", regex=r"^[0-9]{2}:[0-9]{2}:[0-9]{2}$")]

    class Config:
        schema_extra = {
            "example": {
                "name": "서울역",
                "sequence": 1,
                "cumulativeTime": "00:00:00",
            }
        }


class CreateSubwayTimetable(BaseModel):
    station_id: Annotated[str, Field(alias="stationID", pattern=r"^K[0-9]{3}$")]
    start_station_id: Annotated[str, Field(alias="startStationID", pattern=r"^K[0-9]{3}$")]
    terminal_station_id: Annotated[str, Field(alias="terminalStationID", pattern=r"^K[0-9]{3}$")]
    departure_time: Annotated[str, Field(alias="departureTime", regex=r"^[0-9]{2}:[0-9]{2}:[0-9]{2}$")]
    weekday: Annotated[str, Field(alias="weekday", max_length=10)]
    heading: Annotated[str, Field(alias="heading", max_length=10)]

    class Config:
        schema_extra = {
            "example": {
                "stationID": "K101",
                "startStationID": "K101",
                "terminalStationID": "K101",
                "departureTime": "00:00:00",
                "weekday": "weekday",
                "heading": "up",
            }
        }
