from datetime import date
from typing import Callable

from fastapi import APIRouter, Depends
from starlette import status

from event import service
from event.dependancies import (
    create_valid_category,
    get_valid_category,
    create_valid_calendar,
    get_valid_calendar,
)
from event.exceptions import (
    CategoryNotFound,
    CalendarNotFound,
)
from event.schemas import (
    CalendarListResponse,
    CalendarDetailResponse,
    CreateCalendarCategoryRequest,
    CreateCalendarReqeust,
    UpdateCalendarRequest,
    CalendarCategoryListResponse,
    CalendarCategoryDetailResponse,
)
from exceptions import DetailedHTTPException
from model.calendar import CalendarCategory, Calendar
from user.jwt import parse_jwt_user_data

router = APIRouter()


@router.get("/category", response_model=CalendarCategoryListResponse)
async def get_calendar_category_list(
    _: str = Depends(parse_jwt_user_data),
    name: str | None = None,
):
    if name is None:
        data = await service.list_calendar_category()
    else:
        data = await service.list_calendar_category_filter(name)
    mapping_func: Callable[[CalendarCategory], dict[str, int | str]] = lambda x: {
        "id": x.id_,
        "name": x.name,
    }
    return {"data": map(mapping_func, data)}


@router.post(
    "/category",
    status_code=status.HTTP_201_CREATED,
    response_model=CalendarCategoryDetailResponse,
)
async def create_calendar_category(
    new_category: CreateCalendarCategoryRequest = Depends(create_valid_category),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.create_calendar_category(new_category)
    if data is None:
        raise DetailedHTTPException()
    return {
        "id": data.id_,
        "name": data.name,
    }


@router.get("/category/{calendar_category_id}", response_model=CalendarCategoryDetailResponse)
async def get_calendar_category(
    calendar_category_id: int,
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.get_calendar_category(calendar_category_id)
    if data is None:
        raise CategoryNotFound()
    return {
        "id": data.id_,
        "name": data.name,
    }


@router.put(
    "/category/{calendar_category_id}",
    response_model=CalendarCategoryDetailResponse,
)
async def update_calendar_category(
    new_category: CreateCalendarCategoryRequest,
    calendar_category_id: int = Depends(get_valid_category),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.update_calendar_category(
        calendar_category_id,
        new_category,
    )
    if data is None:
        raise DetailedHTTPException()
    return {
        "id": data.id_,
        "name": data.name,
    }


@router.delete(
    "/category/{calendar_category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_calendar_category(
    _: str = Depends(parse_jwt_user_data),
    calendar_category_id: int = Depends(get_valid_category),
):
    await service.delete_calendar_category(calendar_category_id)


@router.get("/category/{calendar_category_id}/event", response_model=CalendarListResponse)
async def get_calendar_list(
    calendar_category_id: int = Depends(get_valid_category),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.get_calendar_list(calendar_category_id)
    mapping_func: Callable[[Calendar], dict[str, int | str | date]] = lambda x: {
        "id": x.id_,
        "title": x.title,
        "description": x.description,
        "start": x.start_date,
        "end": x.end_date,
    }
    return {"data": map(mapping_func, data)}


@router.get(
    "/category/{calendar_category_id}/event/{calendar_id}",
    response_model=CalendarDetailResponse,
)
async def get_calendar(
    calendar_id: int,
    calendar_category_id: int = Depends(get_valid_category),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.get_calendar(calendar_category_id, calendar_id)
    if data is None:
        raise CalendarNotFound()
    return {
        "id": data.id_,
        "title": data.title,
        "description": data.description,
        "start": data.start_date,
        "end": data.end_date,
    }


@router.post(
    "/category/{calendar_category_id}/event",
    status_code=status.HTTP_201_CREATED,
    response_model=CalendarDetailResponse,
)
async def create_calendar(
    new_calendar: CreateCalendarReqeust = Depends(create_valid_calendar),
    calendar_category_id: int = Depends(get_valid_category),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.create_calendar(
        calendar_category_id,
        new_calendar,
    )
    if data is None:
        raise DetailedHTTPException()
    return {
        "id": data.id_,
        "title": data.title,
        "description": data.description,
        "start": data.start_date,
        "end": data.end_date,
    }


@router.put(
    "/category/{calendar_category_id}/event/{calendar_id}",
    response_model=CalendarDetailResponse,
)
async def update_calendar(
    new_calendar: UpdateCalendarRequest,
    calendar_category_id: int = Depends(get_valid_category),
    calendar_id: int = Depends(get_valid_calendar),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.update_calendar(
        calendar_category_id,
        calendar_id,
        new_calendar,
    )
    if data is None:
        raise DetailedHTTPException()
    return {
        "id": data.id_,
        "title": data.title,
        "description": data.description,
        "start": data.start_date,
        "end": data.end_date,
    }


@router.delete(
    "/category/{calendar_category_id}/event/{calendar_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_calendar(
    calendar_id: int,
    calendar_category_id: int = Depends(get_valid_category),
    _: str = Depends(parse_jwt_user_data),
):
    await service.delete_calendar(calendar_category_id, calendar_id)
