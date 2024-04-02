from event import service
from event.exceptions import DuplicateCategoryName, CategoryNotFound, CalendarNotFound
from event.schemas import CreateCalendarCategoryRequest, CreateCalendarReqeust


async def create_valid_category(
    new_category: CreateCalendarCategoryRequest,
) -> CreateCalendarCategoryRequest:
    if await service.get_calendar_category_by_name(new_category.name):
        raise DuplicateCategoryName()
    return new_category


async def get_valid_category(calendar_category_id: int) -> int:
    if await service.get_calendar_category(calendar_category_id) is None:
        raise CategoryNotFound()
    return calendar_category_id


async def create_valid_calendar(
    calendar_category_id: int,
    new_calendar: CreateCalendarReqeust,
) -> CreateCalendarReqeust:
    if await service.get_calendar_category(calendar_category_id) is None:
        raise CategoryNotFound()
    return new_calendar


async def get_valid_calendar(
    calendar_id: int,
) -> int:
    if await service.get_calendar_by_id(calendar_id) is None:
        raise CalendarNotFound()
    return calendar_id
