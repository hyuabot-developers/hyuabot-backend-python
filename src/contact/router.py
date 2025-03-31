from typing import Callable

from fastapi import APIRouter, Depends, Query
from starlette import status

from contact import service
from contact.dependancies import (
    create_valid_category,
    get_valid_category,
    create_valid_contact,
    get_valid_contact,
)
from contact.exceptions import (
    CategoryNotFound,
    ContactNotFound,
)
from contact.schemas import (
    ContactListResponse,
    ContactDetailResponse,
    CreateContactCategoryRequest,
    CreateContactReqeust,
    UpdateContactRequest,
    ContactCategoryListResponse,
    ContactCategoryDetailResponse, ContactListWithCategoryResponse,
)
from exceptions import DetailedHTTPException
from model.contact import PhoneBookCategory, PhoneBook
from user.jwt import parse_jwt_user_data

router = APIRouter()


@router.get("/category", response_model=ContactCategoryListResponse)
async def get_contact_category_list(
    _: str = Depends(parse_jwt_user_data),
    name: str | None = None,
):
    if name is None:
        data = await service.list_contact_category()
    else:
        data = await service.list_contact_category_filter(name)
    mapping_func: Callable[[PhoneBookCategory], dict[str, int | str]] = lambda x: {
        "id": x.id_,
        "name": x.name,
    }
    return {"data": map(mapping_func, data)}


@router.post(
    "/category",
    status_code=status.HTTP_201_CREATED,
    response_model=ContactCategoryDetailResponse,
)
async def create_contact_category(
    new_category: CreateContactCategoryRequest = Depends(create_valid_category),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.create_contact_category(new_category)
    if data is None:
        raise DetailedHTTPException()
    return {
        "id": data.id_,
        "name": data.name,
    }


@router.get("/category/{contact_category_id}", response_model=ContactCategoryDetailResponse)
async def get_contact_category(
    contact_category_id: int,
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.get_contact_category(contact_category_id)
    if data is None:
        raise CategoryNotFound()
    return {
        "id": data.id_,
        "name": data.name,
    }


@router.delete(
    "/category/{contact_category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_contact_category(
    _: str = Depends(parse_jwt_user_data),
    contact_category_id: int = Depends(get_valid_category),
):
    await service.delete_contact_category(contact_category_id)


@router.get("/category/{contact_category_id}/contacts", response_model=ContactListResponse)
async def get_contact_list(
    contact_category_id: int = Depends(get_valid_category),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.get_contact_list(contact_category_id)
    mapping_func: Callable[[PhoneBook], dict[str, int | str]] = lambda x: {
        "id": x.id_,
        "name": x.name,
        "phone": x.phone,
        "campusID": x.campus_id,
    }
    return {"data": map(mapping_func, data)}


@router.get(
    "/category/{contact_category_id}/contacts/{contact_id}",
    response_model=ContactDetailResponse,
)
async def get_contact(
    contact_id: int,
    contact_category_id: int = Depends(get_valid_category),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.get_contact(contact_category_id, contact_id)
    if data is None:
        raise ContactNotFound()
    return {
        "id": data.id_,
        "name": data.name,
        "phone": data.phone,
        "campusID": data.campus_id,
    }


@router.post(
    "/category/{contact_category_id}/contacts",
    status_code=status.HTTP_201_CREATED,
    response_model=ContactDetailResponse,
)
async def create_contact(
    new_contact: CreateContactReqeust = Depends(create_valid_contact),
    contact_category_id: int = Depends(get_valid_category),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.create_contact(
        contact_category_id,
        new_contact,
    )
    if data is None:
        raise DetailedHTTPException()
    return {
        "id": data.id_,
        "name": data.name,
        "phone": data.phone,
        "campusID": data.campus_id,
    }


@router.put(
    "/category/{contact_category_id}/contacts/{contact_id}",
    response_model=ContactDetailResponse,
)
async def update_contact(
    new_contact: UpdateContactRequest,
    contact_category_id: int = Depends(get_valid_category),
    contact_id: int = Depends(get_valid_contact),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.update_contact(
        contact_category_id,
        contact_id,
        new_contact,
    )
    if data is None:
        raise DetailedHTTPException()
    return {
        "id": data.id_,
        "name": data.name,
        "phone": data.phone,
        "campusID": data.campus_id,
    }


@router.delete(
    "/category/{contact_category_id}/contacts/{contact_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_contact(
    contact_id: int,
    contact_category_id: int = Depends(get_valid_category),
    _: str = Depends(parse_jwt_user_data),
):
    await service.delete_contact(contact_category_id, contact_id)


@router.get("/contacts", response_model=ContactListWithCategoryResponse)
async def get_contact_list_with_category(
    _: str = Depends(parse_jwt_user_data),
    campus_id: int | None = Query(None, alias="campusID"),
):
    if campus_id is None:
        data = await service.list_contact()
    else:
        data = await service.list_contact_filter(campus_id)
    mapping_func: Callable[[PhoneBook], dict[str, int | str]] = lambda x: {
        "id": x.id_,
        "name": x.name,
        "phone": x.phone,
        "campusID": x.campus_id,
        "categoryID": x.category_id,
    }
    return {"data": map(mapping_func, data)}
