import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, Field


class CreateBusRouteRequest(BaseModel):
    id_: Annotated[int, Field(alias="id", ge=1)]
    name: Annotated[str, Field(max_length=30, alias="name")]
    type_code: Annotated[str, Field(alias="typeCode")]
    type_name: Annotated[
        str,
        Field(
            alias="typeName",
            max_length=10,
            pattern=r"^(일반형|직행좌석형)시내버스$",
        ),
    ]
    start_stop_id: Annotated[int, Field(alias="start", ge=1)]
    end_stop_id: Annotated[int, Field(alias="end", ge=1)]
    up_first_time: Annotated[datetime.time, Field(alias="upFirstTime")]
    up_last_time: Annotated[datetime.time, Field(alias="upLastTime")]
    down_first_time: Annotated[datetime.time, Field(alias="downFirstTime")]
    down_last_time: Annotated[datetime.time, Field(alias="downLastTime")]
    company_id: Annotated[int, Field(alias="companyID", ge=1)]
    company_name: Annotated[str, Field(alias="companyName", max_length=30)]
    company_telephone: Annotated[
        str,
        Field(
            alias="companyTelephone",
            max_length=20,
            pattern=r"^[0-9]{2,3}-[0-9]{3,4}-[0-9]{4}$",
        ),
    ]
    district_code: Annotated[int, Field(alias="district", ge=1)]

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "1-1",
                "typeCode": 11,
                "typeName": "일반형시내버스",
                "start": 1,
                "end": 2,
                "upFirstTime": "05:00:00+09:00",
                "upLastTime": "23:00:00+09:00",
                "downFirstTime": "05:00:00+09:00",
                "downLastTime": "23:00:00+09:00",
                "companyID": 1,
                "companyName": "서울버스",
                "companyTelephone": "02-1234-5678",
                "district": 1,
            },
        }


class UpdateBusRouteRequest(BaseModel):
    name: Annotated[Optional[str], Field(max_length=30, alias="name")]
    type_code: Annotated[Optional[str], Field(alias="typeCode")]
    type_name: Annotated[
        Optional[str],
        Field(
            alias="typeName",
            max_length=10,
            pattern=r"^(일반형|직행좌석형)시내버스$",
        ),
    ]
    start_stop_id: Annotated[Optional[int], Field(alias="start", ge=1)]
    end_stop_id: Annotated[Optional[int], Field(alias="end", ge=1)]
    up_first_time: Annotated[Optional[datetime.time], Field(alias="upFirstTime")]
    up_last_time: Annotated[Optional[datetime.time], Field(alias="upLastTime")]
    down_first_time: Annotated[Optional[datetime.time], Field(alias="downFirstTime")]
    down_last_time: Annotated[Optional[datetime.time], Field(alias="downLastTime")]
    company_id: Annotated[Optional[int], Field(alias="companyID", ge=1)]
    company_name: Annotated[Optional[str], Field(alias="companyName", max_length=30)]
    company_telephone: Annotated[
        Optional[str],
        Field(
            alias="companyTelephone",
            max_length=20,
            pattern=r"^[0-9]{2,3}-[0-9]{3,4}-[0-9]{4}$",
        ),
    ]
    district_code: Annotated[Optional[int], Field(alias="district", ge=1)]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "1-1",
                "typeCode": 11,
                "typeName": "일반형시내버스",
                "start": 1,
                "end": 2,
                "upFirstTime": "05:00:00+09:00",
                "upLastTime": "23:00:00+09:00",
                "downFirstTime": "05:00:00+09:00",
                "downLastTime": "23:00:00+09:00",
                "companyID": 1,
                "companyName": "서울버스",
                "companyTelephone": "02-1234-5678",
                "district": 1,
            },
        }


class CreateBusStopRequest(BaseModel):
    id_: Annotated[int, Field(alias="id", ge=1)]
    name: Annotated[str, Field(max_length=30, alias="name")]
    district_code: Annotated[int, Field(alias="district", ge=1)]
    mobile_number: Annotated[
        str,
        Field(alias="mobileNumber", max_length=5, pattern=r"^[0-9]{5}$"),
    ]
    region_name: Annotated[str, Field(alias="regionName", max_length=10)]
    latitude: Annotated[float, Field(alias="latitude", ge=-90, le=90)]
    longitude: Annotated[float, Field(alias="longitude", ge=-180, le=180)]

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "서울역",
                "district": 1,
                "mobileNumber": "00001",
                "regionName": "서울역",
                "latitude": 37.123456,
                "longitude": 127.123456,
            },
        }


class UpdateBusStopRequest(BaseModel):
    name: Annotated[Optional[str], Field(max_length=30, alias="name")]
    district_code: Annotated[Optional[int], Field(alias="district", ge=1)]
    mobile_number: Annotated[
        Optional[str],
        Field(alias="mobileNumber", max_length=5, pattern=r"^[0-9]{5}$"),
    ]
    region_name: Annotated[Optional[str], Field(alias="regionName", max_length=10)]
    latitude: Annotated[Optional[float], Field(alias="latitude", ge=-90, le=90)]
    longitude: Annotated[Optional[float], Field(alias="longitude", ge=-180, le=180)]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "서울역",
                "district": 1,
                "mobileNumber": "00001",
                "regionName": "서울역",
                "latitude": 37.123456,
                "longitude": 127.123456,
            },
        }


class CreateBusRouteStopRequest(BaseModel):
    route_id: Annotated[int, Field(alias="routeID", ge=1)]
    stop_id: Annotated[int, Field(alias="stopID", ge=1)]
    sequence: Annotated[int, Field(alias="sequence", ge=1)]
    start_stop_id: Annotated[int, Field(alias="start", ge=1)]

    class Config:
        json_schema_extra = {
            "example": {
                "routeID": 1,
                "stopID": 1,
                "sequence": 1,
                "start": 1,
            },
        }


class UpdateBusRouteStopRequest(BaseModel):
    sequence: Annotated[Optional[int], Field(alias="sequence", ge=1)]
    start_stop_id: Annotated[Optional[int], Field(alias="start", ge=1)]

    class Config:
        json_schema_extra = {
            "example": {
                "sequence": 1,
                "start": 1,
            },
        }


class CreateBusTimetableRequest(BaseModel):
    route_id: Annotated[int, Field(alias="routeID", ge=1)]
    start_stop_id: Annotated[int, Field(alias="start", ge=1)]
    weekdays: Annotated[str, Field(alias="weekdays")]
    departure_time: Annotated[datetime.time, Field(alias="departureTime")]

    class Config:
        json_schema_extra = {
            "example": {
                "routeID": 1,
                "start": 1,
                "weekdays": "weekdays",
                "departureTime": "08:00:00",
            },
        }


class BusRouteListItemResponse(BaseModel):
    route_id: Annotated[int, Field(alias="id", ge=0)]
    route_name: Annotated[str, Field(max_length=30, alias="name")]
    type_name: Annotated[str, Field(max_length=10, alias="type")]


class BusRouteListResponse(BaseModel):
    data: Annotated[list[BusRouteListItemResponse], Field(alias="data")]


class BusRouteFirstLastTimeResponse(BaseModel):
    first_time: Annotated[datetime.time, Field(alias="first")]
    last_time: Annotated[datetime.time, Field(alias="last")]


class BusRouteCompanyResponse(BaseModel):
    company_id: Annotated[int, Field(alias="id", ge=1)]
    company_name: Annotated[str, Field(max_length=30, alias="name")]
    company_telephone: Annotated[str, Field(max_length=20, alias="telephone")]


class BusRouteDetailResponse(BaseModel):
    route_id: Annotated[int, Field(alias="id", ge=1)]
    route_name: Annotated[str, Field(max_length=30, alias="name")]
    type_name: Annotated[str, Field(max_length=10, alias="type")]
    start: Annotated[int, Field(alias="start")]
    end: Annotated[int, Field(alias="end")]
    up: Annotated[BusRouteFirstLastTimeResponse, Field(alias="up")]
    down: Annotated[BusRouteFirstLastTimeResponse, Field(alias="down")]
    company: Annotated[BusRouteCompanyResponse, Field(alias="company")]


class BusStopListItemResponse(BaseModel):
    stop_id: Annotated[int, Field(alias="id", ge=1)]
    stop_name: Annotated[str, Field(max_length=30, alias="name")]


class BusStopListResponse(BaseModel):
    data: Annotated[list[BusStopListItemResponse], Field(alias="data")]


class BusStopDetailResponse(BaseModel):
    stop_id: Annotated[int, Field(alias="id", ge=1)]
    stop_name: Annotated[str, Field(max_length=30, alias="name")]
    district_code: Annotated[int, Field(alias="district", ge=1)]
    mobile_number: Annotated[str, Field(alias="mobileNumber", max_length=5)]
    region_name: Annotated[str, Field(alias="regionName", max_length=30)]
    latitude: Annotated[float, Field(alias="latitude", ge=-90, le=90)]
    longitude: Annotated[float, Field(alias="longitude", ge=-180, le=180)]


class BusRouteStopListItemResponse(BaseModel):
    stop_id: Annotated[int, Field(alias="id", ge=1)]
    sequence: Annotated[int, Field(alias="sequence", ge=0)]
    start_stop_id: Annotated[int, Field(alias="start", ge=1)]


class BusRouteStopListResponse(BaseModel):
    data: Annotated[list[BusRouteStopListItemResponse], Field(alias="data")]


class BusRouteStopDetailResponse(BaseModel):
    stop_id: Annotated[int, Field(alias="id", ge=1)]
    sequence: Annotated[int, Field(alias="sequence", ge=1)]
    start_stop_id: Annotated[int, Field(alias="start", ge=1)]


class BusTimetableListItemResponse(BaseModel):
    route_id: Annotated[int, Field(alias="routeID", ge=1)]
    start_stop_id: Annotated[int, Field(alias="start", ge=1)]
    weekdays: Annotated[str, Field(alias="weekdays")]
    departure_time: Annotated[
        datetime.time,
        Field(alias="departureTime"),
    ]


class BusTimetableListResponse(BaseModel):
    data: Annotated[list[BusTimetableListItemResponse], Field(alias="data")]


class BusTimetableDetailResponse(BaseModel):
    route_id: Annotated[int, Field(alias="routeID", ge=1)]
    start_stop_id: Annotated[int, Field(alias="start", ge=1)]
    weekdays: Annotated[str, Field(alias="weekdays")]
    departure_time: Annotated[
        datetime.time,
        Field(alias="departureTime"),
    ]


class BusRealtimeListItemResponse(BaseModel):
    route_id: Annotated[int, Field(alias="routeID", ge=1)]
    stop_id: Annotated[int, Field(alias="stopID", ge=1)]
    sequence: Annotated[int, Field(alias="sequence", ge=1)]
    remaining_stop: Annotated[int, Field(alias="stop", ge=0)]
    remaining_time: Annotated[
        datetime.timedelta,
        Field(alias="time"),
    ]
    remaining_seat: Annotated[int, Field(alias="seat", ge=-1)]
    low_floor: Annotated[bool, Field(alias="lowFloor")]
    updated_at: Annotated[datetime.datetime, Field(alias="updatedAt")]


class BusRealtimeListResponse(BaseModel):
    data: Annotated[list[BusRealtimeListItemResponse], Field(alias="data")]
