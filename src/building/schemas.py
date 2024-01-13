from typing import Annotated, Optional

from pydantic import BaseModel, Field


class CreateBuildingRequest(BaseModel):
    id: Annotated[str, Field(max_length=15, alias="id")]
    name: Annotated[str, Field(max_length=30, alias="name")]
    campus_id: Annotated[int, Field(alias="campusID")]
    latitude: Annotated[float, Field(alias="latitude")]
    longitude: Annotated[float, Field(alias="longitude")]
    url: Annotated[str, Field(alias="url")]

    class Config:
        json_schema_extra = {
            "example": {
                "id": "Y28",
                "name": "언론정보관",
                "campusID": 2,
                "latitude": 37.123456,
                "longitude": 127.123456,
                "url": "https://blog.naver.com/hyerica4473/223122445405",
            },
        }


class UpdateBuildingRequest(BaseModel):
    name: Annotated[Optional[str], Field(max_length=30, alias="name")]
    latitude: Annotated[Optional[float], Field(alias="latitude")]
    longitude: Annotated[Optional[float], Field(alias="longitude")]
    url: Annotated[Optional[str], Field(alias="url")]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "언론정보관",
                "latitude": 37.123456,
                "longitude": 127.123456,
                "url": "https://blog.naver.com/hyerica4473/223122445405",
            },
        }


class CreateRoomRequest(BaseModel):
    building_id: Annotated[str, Field(max_length=15, alias="buildingID")]
    name: Annotated[str, Field(max_length=30, alias="name")]
    number: Annotated[str, Field(max_length=10, alias="number")]

    class Config:
        json_schema_extra = {
            "example": {
                "buildingID": "Y28",
                "name": "언론정보대학 행정팀",
                "number": "204",
            },
        }


class UpdateRoomRequest(BaseModel):
    name: Annotated[Optional[str], Field(max_length=30, alias="name")]
    floor: Annotated[Optional[str], Field(max_length=10, alias="floor")]
    number: Annotated[Optional[str], Field(max_length=10, alias="number")]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "언론정보대학 행정팀",
                "floor": "2층",
                "number": "204",
            },
        }


class BuildingItemResponse(BaseModel):
    id: Annotated[str, Field(max_length=15, alias="id")]
    name: Annotated[str, Field(max_length=30, alias="name")]
    campus_id: Annotated[int, Field(alias="campusID")]
    latitude: Annotated[float, Field(alias="latitude")]
    longitude: Annotated[float, Field(alias="longitude")]
    url: Annotated[str, Field(alias="url")]

    class Config:
        json_schema_extra = {
            "example": {
                "id": "Y28",
                "name": "언론정보관",
                "campusID": 2,
                "latitude": 37.123456,
                "longitude": 127.123456,
                "url": "https://blog.naver.com/hyerica4473/223122445405",
            },
        }


class BuildingListResponse(BaseModel):
    data: Annotated[list[BuildingItemResponse], Field(alias="data")]

    class Config:
        json_schema_extra = {
            "example": {
                "data": [
                    {
                        "id": "Y28",
                        "name": "언론정보관",
                        "campusID": 2,
                        "latitude": 37.123456,
                        "longitude": 127.123456,
                        "url": "https://blog.naver.com/hyerica4473/223122445405",
                    },
                ],
            },
        }


class RoomItemResponse(BaseModel):
    id: Annotated[int, Field(alias="id")]
    building_id: Annotated[str, Field(max_length=15, alias="buildingID")]
    name: Annotated[str, Field(max_length=30, alias="name")]
    floor: Annotated[str, Field(max_length=10, alias="floor")]
    number: Annotated[str, Field(max_length=10, alias="number")]

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "buildingID": "Y28",
                "name": "언론정보대학 행정팀",
                "floor": "2층",
                "number": "204",
            },
        }


class RoomListResponse(BaseModel):
    data: Annotated[list[RoomItemResponse], Field(alias="data")]

    class Config:
        json_schema_extra = {
            "example": {
                "data": [
                    {
                        "id": 1,
                        "buildingID": "Y28",
                        "name": "언론정보대학 행정팀",
                        "floor": "2층",
                        "number": "204",
                    },
                ],
            },
        }
