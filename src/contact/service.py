import datetime

import pytz
from sqlalchemy import select, insert, delete, update

from database import fetch_all, fetch_one, execute_query
from model.contact import PhoneBookCategory, PhoneBook, PhoneBookVersion
from contact.schemas import (
    CreateContactCategoryRequest,
    CreateContactRequest,
    UpdateContactRequest,
)


async def list_contact_category() -> list[PhoneBookCategory]:
    select_query = select(PhoneBookCategory)
    return await fetch_all(select_query)


async def list_contact_category_filter(name: str) -> list[PhoneBookCategory]:
    select_query = select(PhoneBookCategory).filter(PhoneBookCategory.name.like(f"%{name}%"))
    return await fetch_all(select_query)


async def create_contact_category(
    new_contact_category: CreateContactCategoryRequest,
) -> PhoneBookCategory | None:
    insert_query = (
        insert(PhoneBookCategory)
        .values(
            {
                "name": new_contact_category.name,
            },
        )
    )
    await execute_query(insert_query)
    select_query = select(PhoneBookCategory).where(
        PhoneBookCategory.name == new_contact_category.name
    )
    return await fetch_one(select_query)


async def get_contact_category(contact_category_id: int) -> PhoneBookCategory | None:
    select_query = select(PhoneBookCategory).where(
        PhoneBookCategory.id_ == contact_category_id,
    )
    return await fetch_one(select_query)


async def get_contact_category_by_name(name: str) -> PhoneBookCategory | None:
    select_query = select(PhoneBookCategory).where(PhoneBookCategory.name == name)
    return await fetch_one(select_query)


async def delete_contact_category(contact_category_id: int) -> None:
    delete_query = delete(PhoneBookCategory).where(
        PhoneBookCategory.id_ == contact_category_id,
    )
    await execute_query(delete_query)


async def get_contact_list(contact_category_id: int) -> list[PhoneBook]:
    select_query = select(PhoneBook).where(PhoneBook.category_id == contact_category_id)
    return await fetch_all(select_query)


async def get_contact(
    category_id: int,
    contact_id: int,
) -> PhoneBook | None:
    select_query = select(PhoneBook).where(
        PhoneBook.category_id == category_id,
        PhoneBook.id_ == contact_id,
    )
    return await fetch_one(select_query)


async def get_contact_by_id(contact_id: int) -> PhoneBook | None:
    select_query = select(PhoneBook).where(PhoneBook.id_ == contact_id)
    return await fetch_one(select_query)


async def create_contact(
    category_id: int,
    new_contact: CreateContactRequest,
) -> PhoneBook | None:
    insert_query = (
        insert(PhoneBook)
        .values(
            {
                "category_id": category_id,
                "name": new_contact.name,
                "phone": new_contact.phone,
                "campus_id": new_contact.campus_id,
            },
        )
    )
    delete_version_query = delete(PhoneBookVersion)
    await execute_query(delete_version_query)
    now = datetime.datetime.now(tz=pytz.timezone("Asia/Seoul"))
    insert_version_query = (
        insert(PhoneBookVersion)
        .values(
            {
                "version_id": 1,
                "version_name": now.strftime("%Y-%m-%d %H:%M:%S"),
                "created_at": now,
            },
        )
    )
    await execute_query(insert_version_query)
    await execute_query(insert_query)
    select_query = select(PhoneBook).where(
        PhoneBook.category_id == category_id,
        PhoneBook.name == new_contact.name,
    )
    return await fetch_one(select_query)


async def delete_contact(
    contact_category_id: int,
    contact_id: int,
) -> None:
    delete_query = delete(PhoneBook).where(
        PhoneBook.category_id == contact_category_id,
        PhoneBook.id_ == contact_id,
    )
    await execute_query(delete_query)
    delete_version_query = delete(PhoneBookVersion)
    await execute_query(delete_version_query)
    now = datetime.datetime.now(tz=pytz.timezone("Asia/Seoul"))
    insert_version_query = (
        insert(PhoneBookVersion)
        .values(
            {
                "version_id": 1,
                "version_name": now.strftime("%Y-%m-%d %H:%M:%S"),
                "created_at": now,
            },
        )
    )
    await execute_query(insert_version_query)


async def update_contact(
    contact_category_id: int,
    contact_id: int,
    new_contact: UpdateContactRequest,
) -> PhoneBook | None:
    update_data: dict[str, str | int] = {}
    if new_contact.name:
        update_data["name"] = new_contact.name
    if new_contact.phone:
        update_data["phone"] = new_contact.phone
    if new_contact.campus_id:
        update_data["campus_id"] = new_contact.campus_id

    update_query = (
        update(PhoneBook)
        .where(
            PhoneBook.category_id == contact_category_id,
            PhoneBook.id_ == contact_id,
        )
        .values(update_data)
    )
    delete_version_query = delete(PhoneBookVersion)
    await execute_query(delete_version_query)
    now = datetime.datetime.now(tz=pytz.timezone("Asia/Seoul"))
    insert_version_query = (
        insert(PhoneBookVersion)
        .values(
            {
                "version_id": 1,
                "version_name": now.strftime("%Y-%m-%d %H:%M:%S"),
                "created_at": now,
            },
        )
    )
    await execute_query(insert_version_query)
    await execute_query(update_query)
    select_query = select(PhoneBook).where(
        PhoneBook.category_id == contact_category_id,
        PhoneBook.id_ == contact_id,
    )
    return await fetch_one(select_query)


async def list_contact() -> list[PhoneBook]:
    select_query = select(PhoneBook)
    return await fetch_all(select_query)


async def list_contact_filter(campus_id: int) -> list[PhoneBook]:
    select_query = select(PhoneBook).where(PhoneBook.campus_id == campus_id)
    return await fetch_all(select_query)
