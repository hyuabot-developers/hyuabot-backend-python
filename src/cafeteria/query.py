import datetime
from typing import Optional, Callable

import strawberry
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from database import fetch_all
from model.cafeteria import Menu, Cafeteria


@strawberry.type
class MenuQuery:
    feed_date: datetime.date = strawberry.field(
        description="Feed date",
        name="date",
    )
    time_type: str = strawberry.field(
        description="Time type",
        name="type",
    )
    menu: str = strawberry.field(description="Menu")
    price: str = strawberry.field(description="Price")


@strawberry.type
class CafeteriaRunningTimeQuery:
    breakfast: str | None = strawberry.field(description="Breakfast running time", default=None)
    lunch: str | None = strawberry.field(description="Lunch running time", default=None)
    dinner: str | None = strawberry.field(description="Dinner running time", default=None)


@strawberry.type
class CafeteriaQuery:
    id_: int = strawberry.field(description="Cafeteria ID", name="id")
    name: str = strawberry.field(description="Cafeteria name")
    latitude: float = strawberry.field(description="Cafeteria latitude")
    longitude: float = strawberry.field(description="Cafeteria longitude")
    running_time: CafeteriaRunningTimeQuery = strawberry.field(
        description="Cafeteria running time",
        name="runningTime",
    )
    menu_list: list[MenuQuery] = strawberry.field(
        description="Menu list",
        name="menu",
    )


async def resolve_menu(
    campus_id: Optional[int] = None,
    name: Optional[str] = None,
    date: Optional[datetime.date] = None,
    type_: Optional[list[str]] = None,
) -> list[CafeteriaQuery]:
    cafeteria_conditions = []
    if campus_id is not None:
        cafeteria_conditions.append(Cafeteria.campus_id == campus_id)
    if name is not None:
        cafeteria_conditions.append(Cafeteria.name.like(f"%{name}%"))
    select_query = select(Cafeteria).where(*cafeteria_conditions)
    cafeteria_list: list[Cafeteria] = await fetch_all(select_query)

    menu_conditions = [
        Menu.restaurant_id.in_([cafeteria.id_ for cafeteria in cafeteria_list]),
    ]
    if date is not None:
        menu_conditions.append(Menu.feed_date.in_([date]))
    if type_ is not None:
        menu_conditions.append(Menu.time_type.in_(type_))
    menu_select_query = (
        select(Menu).where(*menu_conditions).options(joinedload(Menu.restaurant))
    )
    menu_list: list[Menu] = await fetch_all(menu_select_query)
    menu_group_dict: dict[int, list[MenuQuery]] = {}
    for menu in menu_list:
        if menu.restaurant_id not in menu_group_dict:
            menu_group_dict[menu.restaurant_id] = []
        menu_group_dict[menu.restaurant_id].append(
            MenuQuery(
                feed_date=menu.feed_date,
                time_type=menu.time_type,
                menu=menu.menu,
                price=menu.price,
            ),
        )

    cafeteria_mapping_func: Callable[[Cafeteria], CafeteriaQuery] = (
        lambda cafeteria: CafeteriaQuery(
            id_=cafeteria.id_,
            name=cafeteria.name,
            latitude=cafeteria.latitude,
            longitude=cafeteria.longitude,
            menu_list=menu_group_dict.get(cafeteria.id_, []),
            running_time=CafeteriaRunningTimeQuery(
                breakfast=cafeteria.breakfast_running_time,
                lunch=cafeteria.lunch_running_time,
                dinner=cafeteria.dinner_running_time,
            ),
        )
    )
    return list(map(cafeteria_mapping_func, cafeteria_list))
