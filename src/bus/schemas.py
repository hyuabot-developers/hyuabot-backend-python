import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, Field


class CreateBusRouteRequest(BaseModel):
    id: Annotated[int, Field(alias="id", ge=1)]
    name: Annotated[str, Field(max_length=30, alias="name")]
    type_code: Annotated[int, Field(alias="typeCode", ge=11, le=15)]
    type_name: Annotated[
        str,
        Field(alias="typeName", max_length=10, regex=r"^(일반형|직행좌석형)시내버스$"),
    ]
    start_stop_id: Annotated[int, Field(alias="start", ge=1)]
    end_stop_id: Annotated[int, Field(alias="end", ge=1)]
    up_first_time: Annotated[
        datetime.time,
        Field(alias="upFirstTime", regex=r"^[0-9]{2}:[0-9]{2}:[0-9]{2}+09:00$"),
    ]
    up_last_time: Annotated[
        datetime.time,
        Field(alias="upLastTime", regex=r"^[0-9]{2}:[0-9]{2}:[0-9]{2}+09:00$"),
    ]
    down_first_time: Annotated[
        datetime.time,
        Field(alias="downFirstTime", regex=r"^[0-9]{2}:[0-9]{2}:[0-9]{2}+09:00$"),
    ]
    down_last_time: Annotated[
        datetime.time,
        Field(alias="downLastTime", regex=r"^[0-9]{2}:[0-9]{2}:[0-9]{2}+09:00$"),
    ]
    company_id: Annotated[int, Field(alias="companyID", ge=1)]
    company_name: Annotated[str, Field(alias="companyName", max_length=30)]
    company_telephone: Annotated[
        str,
        Field(
            alias="companyTelephone",
            max_length=20,
            regex=r"^[0-9]{2,3}-[0-9]{3,4}-[0-9]{4}$",
        ),
    ]

    class Config:
        schema_extra = {
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
            },
        }


class UpdateBusRouteRequest(BaseModel):
    name: Annotated[Optional[str], Field(max_length=30, alias="name")]
    type_code: Annotated[Optional[int], Field(alias="typeCode", ge=11, le=15)]
    type_name: Annotated[
        Optional[str],
        Field(alias="typeName", max_length=10, regex=r"^(일반형|직행좌석형)시내버스$"),
    ]
    start_stop_id: Annotated[Optional[int], Field(alias="start", ge=1)]
    end_stop_id: Annotated[Optional[int], Field(alias="end", ge=1)]
    up_first_time: Annotated[
        Optional[datetime.time],
        Field(alias="upFirstTime", regex=r"^[0-9]{2}:[0-9]{2}:[0-9]{2}+09:00$"),
    ]
    up_last_time: Annotated[
        Optional[datetime.time],
        Field(alias="upLastTime", regex=r"^[0-9]{2}:[0-9]{2}:[0-9]{2}+09:00$"),
    ]
    down_first_time: Annotated[
        Optional[datetime.time],
        Field(alias="downFirstTime", regex=r"^[0-9]{2}:[0-9]{2}:[0-9]{2}+09:00$"),
    ]
    down_last_time: Annotated[
        Optional[datetime.time],
        Field(alias="downLastTime", regex=r"^[0-9]{2}:[0-9]{2}:[0-9]{2}+09:00$"),
    ]
    company_id: Annotated[Optional[int], Field(alias="companyID", ge=1)]
    company_name: Annotated[Optional[str], Field(alias="companyName", max_length=30)]
    company_telephone: Annotated[
        Optional[str],
        Field(
            alias="companyTelephone",
            max_length=20,
            regex=r"^[0-9]{2,3}-[0-9]{3,4}-[0-9]{4}$",
        ),
    ]

    class Config:
        schema_extra = {
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
            },
        }


class CreateBusStopRequest(BaseModel):
    id: Annotated[int, Field(alias="id", ge=1)]
    name: Annotated[str, Field(max_length=30, alias="name")]
    district_code: Annotated[int, Field(alias="district", ge=1)]
    mobile_number: Annotated[
        str,
        Field(alias="mobileNumber", max_length=5, regex=r"^[0-9]{5}$"),
    ]
    region_name: Annotated[str, Field(alias="regionName", max_length=30)]
    latitude: Annotated[float, Field(alias="latitude", ge=-90, le=90)]
    longitude: Annotated[float, Field(alias="longitude", ge=-180, le=180)]

    class Config:
        schema_extra = {
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
        Field(alias="mobileNumber", max_length=5, regex=r"^[0-9]{5}$"),
    ]
    region_name: Annotated[Optional[str], Field(alias="regionName", max_length=30)]
    latitude: Annotated[Optional[float], Field(alias="latitude", ge=-90, le=90)]
    longitude: Annotated[Optional[float], Field(alias="longitude", ge=-180, le=180)]

    class Config:
        schema_extra = {
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
        schema_extra = {
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
        schema_extra = {
            "example": {
                "sequence": 1,
                "start": 1,
            },
        }


class CreateBusTimetableRequest(BaseModel):
    route_id: Annotated[int, Field(alias="routeID", ge=1)]
    start_stop_id: Annotated[int, Field(alias="start", ge=1)]
    weekdays: Annotated[
        str,
        Field(alias="weekdays", regex=r"^[weekdays|saturday|sunday]$"),
    ]
    departure_time: Annotated[
        str,
        Field(alias="departureTime", regex=r"^[0-9]{2}:[0-9]{2}:[0-9]{2}$"),
    ]

    class Config:
        schema_extra = {
            "example": {
                "routeID": 1,
                "start": 1,
                "weekdays": "weekdays",
                "departureTime": "08:00:00",
            },
        }
