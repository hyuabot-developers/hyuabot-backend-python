import datetime

from sqlalchemy import select, update, insert, delete

from cafeteria.schemas import (
    UpdateCafeteriaRequest,
    CreateCafeteriaRequest,
    UpdateCafeteriaMenuRequest,
    CreateCafeteriaMenuRequest,
)
from database import fetch_all, fetch_one, execute_query
from model.cafeteria import Cafeteria, Menu


async def list_cafeteria() -> list[Cafeteria]:
    select_query = select(Cafeteria)
    return await fetch_all(select_query)


async def list_cafeteria_filter(campus_id: int) -> list[Cafeteria]:
    select_query = select(Cafeteria).filter(
        Cafeteria.campus_id == campus_id,
    )
    return await fetch_all(select_query)


async def create_cafeteria(
    new_cafeteria: CreateCafeteriaRequest,
) -> Cafeteria | None:
    insert_query = (
        insert(Cafeteria)
        .values(
            {
                "restaurant_id": new_cafeteria.id_,
                "restaurant_name": new_cafeteria.name,
                "campus_id": new_cafeteria.campus_id,
                "latitude": new_cafeteria.latitude,
                "longitude": new_cafeteria.longitude,
            },
        )
        .returning(Cafeteria)
    )
    return await fetch_one(insert_query)


async def get_cafeteria(cafeteria_id: int) -> Cafeteria | None:
    select_query = select(Cafeteria).where(Cafeteria.id_ == cafeteria_id)
    return await fetch_one(select_query)


async def update_cafeteria(
    cafeteria_id: int,
    new_cafeteria: UpdateCafeteriaRequest,
) -> Cafeteria | None:
    update_query = (
        update(Cafeteria)
        .where(Cafeteria.id_ == cafeteria_id)
        .values(
            {
                "name": new_cafeteria.name,
                "latitude": new_cafeteria.latitude,
                "longitude": new_cafeteria.longitude,
            },
        )
        .returning(Cafeteria)
    )

    return await fetch_one(update_query)


async def delete_cafeteria(cafeteria_id: int) -> None:
    delete_query = delete(Cafeteria).where(Cafeteria.id_ == cafeteria_id)
    await execute_query(delete_query)


async def get_list_menu_by_cafeteria_id(cafeteria_id: int) -> list[Menu]:
    select_query = select(Menu).where(Menu.restaurant_id == cafeteria_id)
    return await fetch_all(select_query)


async def get_list_menu_by_cafeteria_id_and_date(
    cafeteria_id: int,
    date: datetime.date,
) -> list[Menu]:
    select_query = select(Menu).where(
        Menu.restaurant_id == cafeteria_id,
        Menu.feed_date == date,
    )
    return await fetch_all(select_query)


async def get_menu(
    cafeteria_id: int,
    date: datetime.date,
    time: str,
    menu: str,
) -> Menu | None:
    select_query = select(Menu).where(
        Menu.restaurant_id == cafeteria_id,
        Menu.feed_date == date,
        Menu.time_type == time,
        Menu.menu == menu,
    )
    return await fetch_one(select_query)


async def create_menu(
    cafeteria_id: int,
    new_menu: CreateCafeteriaMenuRequest,
) -> Menu | None:
    insert_query = (
        insert(Menu)
        .values(
            {
                "restaurant_id": cafeteria_id,
                "feed_date": new_menu.date,
                "time_type": new_menu.time,
                "menu_food": new_menu.menu,
                "menu_price": new_menu.price,
            },
        )
        .returning(Menu)
    )
    return await fetch_one(insert_query)


async def delete_menu(
    cafeteria_id: int,
    date: datetime.date,
    time: str,
    menu: str,
) -> None:
    delete_query = delete(Menu).where(
        Menu.restaurant_id == cafeteria_id,
        Menu.feed_date == date,
        Menu.time_type == time,
        Menu.menu == menu,
    )
    await execute_query(delete_query)


async def update_menu(
    cafeteria_id: int,
    date: datetime.date,
    time: str,
    menu: str,
    payload: UpdateCafeteriaMenuRequest,
) -> Menu | None:
    update_query = (
        update(Menu)
        .where(
            Menu.restaurant_id == cafeteria_id,
            Menu.feed_date == date,
            Menu.time_type == time,
            Menu.menu == menu,
        )
        .values(
            {
                "price": payload.price,
            },
        )
        .returning(Menu)
    )

    return await fetch_one(update_query)
