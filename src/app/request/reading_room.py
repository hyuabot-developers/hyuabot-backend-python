from typing import Annotated, Optional

from pydantic import BaseModel, Field


class CreateReadingRoomRequest(BaseModel):
    campus_id: Annotated[int, Field(alias="campusID")]
    id: Annotated[int, Field(alias="id", ge=1)]
    name: Annotated[str, Field(max_length=30, alias="name")]
    active: Annotated[bool, Field(default=False)]
    reservable: Annotated[bool, Field(default=False)]
    total_seats: Annotated[int, Field(alias="total", ge=1)]
    active_seats: Annotated[int, Field(alias="active", ge=0)]

    class Config:
        schema_extra = {
            "example": {
                "campusID": 1,
                "id": 1,
                "name": "제1열람실",
                "active": False,
                "reservable": False,
                "total": 100,
                "active_total": 0,
            }
        }


class UpdateReadingRoomRequest(BaseModel):
    active: Annotated[Optional[bool], Field()]
    reservable: Annotated[Optional[bool], Field()]
    total_seats: Annotated[Optional[int], Field(alias="total", ge=1)]
    active_seats: Annotated[Optional[int], Field(alias="active", ge=0)]

    class Config:
        schema_extra = {
            "example": {
                "active": False,
                "reservable": False,
                "total": 100,
                "active_total": 0,
            }
        }
