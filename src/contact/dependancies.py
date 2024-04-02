from contact import service
from contact.exceptions import DuplicateCategoryName, CategoryNotFound, ContactNotFound
from contact.schemas import CreateContactCategoryRequest, CreateContactReqeust


async def create_valid_category(
    new_category: CreateContactCategoryRequest,
) -> CreateContactCategoryRequest:
    if await service.get_contact_category_by_name(new_category.name):
        raise DuplicateCategoryName()
    return new_category


async def get_valid_category(contact_category_id: int) -> int:
    if await service.get_contact_category(contact_category_id) is None:
        raise CategoryNotFound()
    return contact_category_id


async def create_valid_contact(
    contact_category_id: int,
    new_contact: CreateContactReqeust,
) -> CreateContactReqeust:
    if await service.get_contact_category(contact_category_id) is None:
        raise CategoryNotFound()
    return new_contact


async def get_valid_contact(
    contact_id: int,
) -> int:
    if await service.get_contact_by_id(contact_id) is None:
        raise ContactNotFound()
    return contact_id
