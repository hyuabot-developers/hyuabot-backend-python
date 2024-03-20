import datetime
from typing import Callable

from fastapi import APIRouter, Depends
from starlette import status

from cafeteria import service
from cafeteria.dependancies import (
    create_valid_cafeteria,
    get_valid_cafeteria,
    create_valid_menu,
)
from cafeteria.exceptions import (
    CafeteriaNotFound,
    MenuNotFound,
)
from cafeteria.schemas import (
    CafeteriaListResponse,
    CafeteriaDetailResponse,
    CreateCafeteriaRequest,
    CreateCafeteriaMenuRequest,
    UpdateCafeteriaMenuRequest,
    CafeteriaMenuListResponse,
    CafeteriaMenuResponse,
    UpdateCafeteriaRequest,
)
from exceptions import DetailedHTTPException
from model.cafeteria import Cafeteria, Menu
from user.jwt import parse_jwt_user_data

router = APIRouter()


@router.get("", response_model=CafeteriaListResponse)
async def get_cafeteria_list(
    _: str = Depends(parse_jwt_user_data),
    campus: int | None = None,
):
    if campus is None:
        data = await service.list_cafeteria()
    else:
        data = await service.list_cafeteria_filter(campus)
    mapping_func: Callable[[Cafeteria], dict[str, int | str]] = lambda x: {
        "id": x.id_,
        "name": x.name,
    }
    return {"data": map(mapping_func, data)}


@router.get("/{cafeteria_id}", response_model=CafeteriaDetailResponse)
async def get_cafeteria(
    cafeteria_id: int,
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.get_cafeteria(cafeteria_id)
    if data is None:
        raise CafeteriaNotFound()
    return {
        "id": data.id_,
        "name": data.name,
        "campusID": data.campus_id,
        "latitude": data.latitude,
        "longitude": data.longitude,
        "runningTime": {
            "breakfast": data.breakfast_running_time,
            "lunch": data.lunch_running_time,
            "dinner": data.dinner_running_time,
        },
    }


@router.post(
    "",
    response_model=CafeteriaDetailResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_cafeteria(
    new_cafeteria: CreateCafeteriaRequest,
    _: str = Depends(parse_jwt_user_data),
):
    new_cafeteria = await create_valid_cafeteria(new_cafeteria)
    data = await service.create_cafeteria(new_cafeteria)
    if data is None:
        raise DetailedHTTPException()
    return {
        "id": data.id_,
        "name": data.name,
        "campusID": data.campus_id,
        "latitude": data.latitude,
        "longitude": data.longitude,
        "runningTime": {
            "breakfast": data.breakfast_running_time,
            "lunch": data.lunch_running_time,
            "dinner": data.dinner_running_time,
        },
    }


@router.patch("/{cafeteria_id}", response_model=CafeteriaDetailResponse)
async def update_cafeteria(
    new_cafeteria: UpdateCafeteriaRequest,
    cafeteria_id: int = Depends(get_valid_cafeteria),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.update_cafeteria(cafeteria_id, new_cafeteria)
    if data is None:
        raise DetailedHTTPException()
    return {
        "id": data.id_,
        "name": data.name,
        "campusID": data.campus_id,
        "latitude": data.latitude,
        "longitude": data.longitude,
        "runningTime": {
            "breakfast": data.breakfast_running_time,
            "lunch": data.lunch_running_time,
            "dinner": data.dinner_running_time,
        },
    }


@router.delete("/{cafeteria_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cafeteria(
    cafeteria_id: int = Depends(get_valid_cafeteria),
    _: str = Depends(parse_jwt_user_data),
):
    await service.delete_cafeteria(cafeteria_id)
    return None


@router.get(
    "/{cafeteria_id}/menu",
    response_model=CafeteriaMenuListResponse,
)
async def get_cafeteria_menu(
    date: datetime.date | None = None,
    cafeteria_id: int = Depends(get_valid_cafeteria),
    _: str = Depends(parse_jwt_user_data),
):
    if date is None:
        data = await service.get_list_menu_by_cafeteria_id(cafeteria_id)
    else:
        data = await service.get_list_menu_by_cafeteria_id_and_date(
            cafeteria_id,
            date,
        )
    mapping_func: Callable[[Menu], dict[str, int | str | datetime.date]] = lambda x: {
        "date": x.feed_date,
        "time": x.time_type,
        "menu": x.menu,
        "price": x.price,
    }
    return {"data": map(mapping_func, data)}


@router.post(
    "/{cafeteria_id}/menu",
    response_model=CafeteriaMenuResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_cafeteria_menu(
    new_menu: CreateCafeteriaMenuRequest,
    _cafeteria_id: int = Depends(get_valid_cafeteria),
    _: str = Depends(parse_jwt_user_data),
):
    new_menu = await create_valid_menu(_cafeteria_id, new_menu)
    data = await service.create_menu(_cafeteria_id, new_menu)
    if data is None:
        raise DetailedHTTPException()
    return {
        "date": data.feed_date,
        "time": data.time_type,
        "menu": data.menu,
        "price": data.price,
    }


@router.get(
    "/{cafeteria_id}/menu/{feed_date}/{time_type}/{menu_food}",
    response_model=CafeteriaMenuResponse,
)
async def get_cafeteria_menu_item(
    feed_date: datetime.date,
    time_type: str,
    menu_food: str,
    cafeteria_id: int = Depends(get_valid_cafeteria),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.get_menu(
        cafeteria_id,
        feed_date,
        time_type,
        menu_food,
    )
    if data is None:
        raise MenuNotFound()
    return {
        "date": data.feed_date,
        "time": data.time_type,
        "menu": data.menu,
        "price": data.price,
    }


@router.patch(
    "/{cafeteria_id}/menu/{feed_date}/{time_type}/{menu_food}",
    response_model=CafeteriaMenuResponse,
)
async def update_cafeteria_menu(
    feed_date: datetime.date,
    time_type: str,
    menu_food: str,
    new_menu: UpdateCafeteriaMenuRequest,
    cafeteria_id: int = Depends(get_valid_cafeteria),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.get_menu(
        cafeteria_id,
        feed_date,
        time_type,
        menu_food,
    )
    if data is None:
        raise MenuNotFound()
    data = await service.update_menu(
        cafeteria_id,
        feed_date,
        time_type,
        menu_food,
        new_menu,
    )
    if data is None:
        raise DetailedHTTPException()
    return {
        "date": data.feed_date,
        "time": data.time_type,
        "menu": data.menu,
        "price": data.price,
    }


@router.delete(
    "/{cafeteria_id}/menu/{feed_date}/{time_type}/{menu_food}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_cafeteria_menu(
    feed_date: datetime.date,
    time_type: str,
    menu_food: str,
    cafeteria_id: int = Depends(get_valid_cafeteria),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.get_menu(
        cafeteria_id,
        feed_date,
        time_type,
        menu_food,
    )
    if data is None:
        raise MenuNotFound()
    await service.delete_menu(
        cafeteria_id,
        feed_date,
        time_type,
        menu_food,
    )
    return None
