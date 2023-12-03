from notice import service
from notice.exceptions import DuplicateCategoryName, CategoryNotFound
from notice.schemas import CreateNoticeCategoryRequest, CreateNoticeReqeust


async def create_valid_category(
    new_category: CreateNoticeCategoryRequest,
) -> CreateNoticeCategoryRequest:
    if await service.get_notice_category_by_name(new_category.name):
        raise DuplicateCategoryName()
    return new_category


async def get_valid_category(category_id: int) -> int:
    if await service.get_notice_category(category_id) is None:
        raise CategoryNotFound()
    return category_id


async def create_valid_notice(
    category_id: int,
    new_notice: CreateNoticeReqeust,
) -> CreateNoticeReqeust:
    if await service.get_notice_category(category_id) is None:
        raise CategoryNotFound()
    return new_notice
