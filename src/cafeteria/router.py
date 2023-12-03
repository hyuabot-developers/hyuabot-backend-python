import datetime

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
    return {
        "data": map(
            lambda x: {
                "id": x["restaurant_id"],
                "name": x["restaurant_name"],
            },
            data,
        ),
    }


@router.get("/{cafeteria_id}", response_model=CafeteriaDetailResponse)
async def get_cafeteria(
    cafeteria_id: int,
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.get_cafeteria(cafeteria_id)
    if data is None:
        raise CafeteriaNotFound()
    return {
        "id": data["restaurant_id"],
        "name": data["restaurant_name"],
        "campus": data["campus_id"],
        "latitude": data["latitude"],
        "longitude": data["longitude"],
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
        "id": data["restaurant_id"],
        "name": data["restaurant_name"],
        "campus": data["campus_id"],
        "latitude": data["latitude"],
        "longitude": data["longitude"],
    }


@router.patch("/{cafeteria_id}", response_model=CafeteriaDetailResponse)
async def update_cafeteria(
    new_cafeteria: UpdateCafeteriaRequest,
    cafeteria_id: int = Depends(get_valid_cafeteria),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.update_cafeteria(cafeteria_id, new_cafeteria)
    if data is None:
        raise CafeteriaNotFound()
    return {
        "id": data["restaurant_id"],
        "name": data["restaurant_name"],
        "campus": data["campus_id"],
        "latitude": data["latitude"],
        "longitude": data["longitude"],
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
    cafeteria_id: int = Depends(get_valid_cafeteria),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.get_list_menu_by_cafeteria_id(cafeteria_id)
    return {
        "data": map(
            lambda x: {
                "date": x["feed_date"],
                "time": x["time_type"],
                "menu": x["menu_food"],
                "price": x["menu_price"],
            },
            data,
        ),
    }


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
        "date": data["feed_date"],
        "time": data["time_type"],
        "menu": data["menu_food"],
        "price": data["menu_price"],
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
        "date": data["feed_date"],
        "time": data["time_type"],
        "menu": data["menu_food"],
        "price": data["menu_price"],
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
    await service.update_menu(
        cafeteria_id,
        feed_date,
        time_type,
        menu_food,
        new_menu,
    )
    return {
        "date": data["feed_date"],
        "time": data["time_type"],
        "menu": data["menu_food"],
        "price": data["menu_price"],
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
    await service.delete_menu(
        cafeteria_id,
        feed_date,
        time_type,
        menu_food,
    )
    return None
