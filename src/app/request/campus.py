from typing import Annotated

from pydantic import BaseModel, Field


class CreateCampusRequest(BaseModel):
    id: Annotated[int, Field(alias="id", ge=1)]
    name: Annotated[str, Field(max_length=30, alias="name")]

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "서울캠퍼스",
            }
        }


class UpdateCampusRequest(BaseModel):
    name: Annotated[str, Field(max_length=30, alias="name")]

    class Config:
        schema_extra = {
            "example": {
                "name": "서울캠퍼스",
            }
        }
