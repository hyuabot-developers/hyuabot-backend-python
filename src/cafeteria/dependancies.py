from cafeteria import service
from cafeteria.exceptions import (
    DuplicateCafeteriaID,
    InvalidCampusID,
    CafeteriaNotFound,
    DuplicateMenuID,
)
from cafeteria.schemas import CreateCafeteriaRequest, CreateCafeteriaMenuRequest
from campus.service import get_campus


async def create_valid_cafeteria(
    new_cafeteria: CreateCafeteriaRequest,
) -> CreateCafeteriaRequest:
    if await service.get_cafeteria(new_cafeteria.id):
        raise DuplicateCafeteriaID()
    elif await get_campus(new_cafeteria.campus_id) is None:
        raise InvalidCampusID()
    return new_cafeteria


async def get_valid_cafeteria(cafeteria_id: int) -> int:
    if await service.get_cafeteria(cafeteria_id) is None:
        raise CafeteriaNotFound()
    return cafeteria_id


async def create_valid_menu(
    cafeteria_id: int,
    new_menu: CreateCafeteriaMenuRequest,
) -> CreateCafeteriaMenuRequest:
    if await service.get_menu(
        cafeteria_id,
        new_menu.date,
        new_menu.time,
        new_menu.menu,
    ):
        raise DuplicateMenuID()
    return new_menu
