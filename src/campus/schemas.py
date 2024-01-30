from typing import Annotated

from pydantic import BaseModel, Field


class CreateCampusRequest(BaseModel):
    id_: Annotated[int, Field(alias="id", ge=1)]
    name: Annotated[str, Field(max_length=30, alias="name")]

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "서울캠퍼스",
            },
        }


class UpdateCampusRequest(BaseModel):
    name: Annotated[str, Field(max_length=30, alias="name")]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "서울캠퍼스",
            },
        }


class CampusDetailResponse(BaseModel):
    campus_id: Annotated[int, Field(alias="id", ge=1)]
    campus_name: Annotated[str, Field(max_length=30, alias="name")]


class CampusListResponse(BaseModel):
    data: Annotated[list[CampusDetailResponse], Field(alias="data")]
