from typing import Annotated, Optional

from pydantic import BaseModel, Field


class CreateContactCategoryRequest(BaseModel):
    name: Annotated[str, Field(max_length=20, alias="name")]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "전체",
            },
        }


class CreateContactRequest(BaseModel):
    name: Annotated[str, Field(alias="name")]
    phone: Annotated[str, Field(max_length=30, alias="phone")]
    campus_id: Annotated[int, Field(ge=1, alias="campusID")]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "홍길동",
                "phone": "010-1234-5678",
                "campusID": 1,
            },
        }


class UpdateContactRequest(BaseModel):
    name: Annotated[Optional[str], Field(alias="name")]
    phone: Annotated[Optional[str], Field(max_length=30, alias="phone")]
    campus_id: Annotated[Optional[int], Field(ge=1, alias="campusID")]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "홍길동",
                "phone": "010-1234-5678",
                "campusID": 1,
            },
        }


class ContactCategoryDetailResponse(BaseModel):
    id_: Annotated[int, Field(alias="id", ge=0)]
    name: Annotated[str, Field(max_length=20, alias="name")]


class ContactCategoryListResponse(BaseModel):
    data: Annotated[list[ContactCategoryDetailResponse], Field(alias="data")]


class ContactDetailResponse(BaseModel):
    id_: Annotated[int, Field(alias="id", ge=0)]
    name: Annotated[str, Field(alias="name")]
    phone: Annotated[str, Field(max_length=30, alias="phone")]
    campus_id: Annotated[int, Field(ge=1, alias="campusID")]


class ContactListResponse(BaseModel):
    data: Annotated[list[ContactDetailResponse], Field(alias="data")]


class ContactDetailWithCategoryResponse(BaseModel):
    id_: Annotated[int, Field(alias="id", ge=0)]
    name: Annotated[str, Field(alias="name")]
    phone: Annotated[str, Field(max_length=30, alias="phone")]
    category_id: Annotated[int, Field(alias="categoryID", ge=0)]
    campus_id: Annotated[int, Field(ge=1, alias="campusID")]


class ContactListWithCategoryResponse(BaseModel):
    data: Annotated[list[ContactDetailWithCategoryResponse], Field(alias="data")]
