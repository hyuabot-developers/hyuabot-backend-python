import datetime

import pytz
from sqlalchemy import select, insert, delete, update

from database import fetch_all, fetch_one, execute_query
from model.calendar import CalendarCategory, Calendar, CalendarVersion
from event.schemas import (
    CreateCalendarCategoryRequest,
    CreateCalendarReqeust,
    UpdateCalendarRequest,
)


async def list_calendar_category() -> list[CalendarCategory]:
    select_query = select(CalendarCategory)
    return await fetch_all(select_query)


async def list_calendar_category_filter(name: str) -> list[CalendarCategory]:
    select_query = select(CalendarCategory).filter(CalendarCategory.name.like(f"%{name}%"))
    return await fetch_all(select_query)


async def create_calendar_category(
    new_calendar_category: CreateCalendarCategoryRequest,
) -> CalendarCategory | None:
    insert_query = (
        insert(CalendarCategory)
        .values(
            {
                "name": new_calendar_category.name,
            },
        )
        .returning(CalendarCategory)
    )
    return await fetch_one(insert_query)


async def get_calendar_category(calendar_category_id: int) -> CalendarCategory | None:
    select_query = select(CalendarCategory).where(
        CalendarCategory.id_ == calendar_category_id,
    )
    return await fetch_one(select_query)


async def get_calendar_category_by_name(name: str) -> CalendarCategory | None:
    select_query = select(CalendarCategory).where(CalendarCategory.name == name)
    return await fetch_one(select_query)


async def delete_calendar_category(calendar_category_id: int) -> None:
    delete_query = delete(CalendarCategory).where(
        CalendarCategory.id_ == calendar_category_id,
    )
    await execute_query(delete_query)


async def get_calendar_list(calendar_category_id: int) -> list[Calendar]:
    select_query = select(Calendar).where(Calendar.category_id == calendar_category_id)
    return await fetch_all(select_query)


async def get_calendar(
    category_id: int,
    calendar_id: int,
) -> Calendar | None:
    select_query = select(Calendar).where(
        Calendar.category_id == category_id,
        Calendar.id_ == calendar_id,
    )
    return await fetch_one(select_query)


async def get_calendar_by_id(calendar_id: int) -> Calendar | None:
    select_query = select(Calendar).where(Calendar.id_ == calendar_id)
    return await fetch_one(select_query)


async def create_calendar(
    category_id: int,
    new_calendar: CreateCalendarReqeust,
) -> Calendar | None:
    insert_query = (
        insert(Calendar)
        .values(
            {
                "category_id": category_id,
                "title": new_calendar.title,
                "description": new_calendar.description,
                "start_date": new_calendar.start_date,
                "end_date": new_calendar.end_date,
            },
        )
        .returning(Calendar)
    )
    delete_version_query = delete(CalendarVersion)
    await execute_query(delete_version_query)
    now = datetime.datetime.now(tz=pytz.timezone("Asia/Seoul"))
    insert_version_query = (
        insert(CalendarVersion)
        .values(
            {
                "version_id": 1,
                "version_name": now.strftime("%Y-%m-%d %H:%M:%S"),
                "created_at": now,
            },
        )
        .returning(CalendarVersion)
    )
    await execute_query(insert_version_query)
    return await fetch_one(insert_query)


async def delete_calendar(
    calendar_category_id: int,
    calendar_id: int,
) -> None:
    delete_query = delete(Calendar).where(
        Calendar.category_id == calendar_category_id,
        Calendar.id_ == calendar_id,
    )
    await execute_query(delete_query)
    delete_version_query = delete(CalendarVersion)
    await execute_query(delete_version_query)
    now = datetime.datetime.now(tz=pytz.timezone("Asia/Seoul"))
    insert_version_query = (
        insert(CalendarVersion)
        .values(
            {
                "version_id": 1,
                "version_name": now.strftime("%Y-%m-%d %H:%M:%S"),
                "created_at": now,
            },
        )
        .returning(CalendarVersion)
    )
    await execute_query(insert_version_query)


async def update_calendar(
    calendar_category_id: int,
    calendar_id: int,
    new_calendar: UpdateCalendarRequest,
) -> Calendar | None:
    update_data: dict[str, str | datetime.date] = {}
    if new_calendar.title:
        update_data["title"] = new_calendar.title
    if new_calendar.description:
        update_data["description"] = new_calendar.description
    if new_calendar.start_date:
        update_data["start_date"] = new_calendar.start_date
    if new_calendar.end_date:
        update_data["end_date"] = new_calendar.end_date
    update_query = (
        update(Calendar)
        .where(
            Calendar.category_id == calendar_category_id,
            Calendar.id_ == calendar_id,
        )
        .values(update_data)
        .returning(Calendar)
    )
    delete_version_query = delete(CalendarVersion)
    await execute_query(delete_version_query)
    now = datetime.datetime.now(tz=pytz.timezone("Asia/Seoul"))
    insert_version_query = (
        insert(CalendarVersion)
        .values(
            {
                "version_id": 1,
                "version_name": now.strftime("%Y-%m-%d %H:%M:%S"),
                "created_at": now,
            },
        )
        .returning(CalendarVersion)
    )
    await execute_query(insert_version_query)
    return await fetch_one(update_query)
