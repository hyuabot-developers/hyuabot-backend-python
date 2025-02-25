import datetime

from sqlalchemy import select, insert, delete, update

from database import fetch_all, fetch_one, execute_query
from model.notice import NoticeCategory, Notice
from notice.schemas import (
    CreateNoticeCategoryRequest,
    CreateNoticeReqeust,
    UpdateNoticeRequest,
)


async def list_notice_category() -> list[NoticeCategory]:
    select_query = select(NoticeCategory)
    return await fetch_all(select_query)


async def list_notice_category_filter(name: str) -> list[NoticeCategory]:
    select_query = select(NoticeCategory).filter(NoticeCategory.name.like(f"%{name}%"))
    return await fetch_all(select_query)


async def create_notice_category(
    new_notice_category: CreateNoticeCategoryRequest,
) -> NoticeCategory | None:
    insert_query = (
        insert(NoticeCategory)
        .values(
            {
                "name": new_notice_category.name,
            },
        )
    )
    await execute_query(insert_query)
    select_query = select(NoticeCategory).where(
        NoticeCategory.name == new_notice_category.name,
    )
    return await fetch_one(select_query)


async def get_notice_category(notice_category_id: int) -> NoticeCategory | None:
    select_query = select(NoticeCategory).where(
        NoticeCategory.id_ == notice_category_id,
    )
    return await fetch_one(select_query)


async def get_notice_category_by_name(name: str) -> NoticeCategory | None:
    select_query = select(NoticeCategory).where(NoticeCategory.name == name)
    return await fetch_one(select_query)


async def delete_notice_category(notice_category_id: int) -> None:
    delete_query = delete(NoticeCategory).where(
        NoticeCategory.id_ == notice_category_id,
    )
    await execute_query(delete_query)


async def get_notice_list(notice_category_id: int) -> list[Notice]:
    select_query = select(Notice).where(Notice.category_id == notice_category_id)
    return await fetch_all(select_query)


async def get_notice(
    category_id: int,
    notice_id: int,
) -> Notice | None:
    select_query = select(Notice).where(
        Notice.category_id == category_id,
        Notice.id_ == notice_id,
    )
    return await fetch_one(select_query)


async def get_notice_by_id(notice_id: int) -> Notice | None:
    select_query = select(Notice).where(Notice.id_ == notice_id)
    return await fetch_one(select_query)


async def create_notice(
    user_id: str,
    category_id: int,
    new_notice: CreateNoticeReqeust,
) -> Notice | None:
    insert_query = (
        insert(Notice)
        .values(
            {
                "user_id": user_id,
                "category_id": category_id,
                "title": new_notice.title,
                "url": new_notice.url,
                "expired_at": new_notice.expired_at,
            },
        )
    )
    await execute_query(insert_query)
    select_query = select(Notice).where(
        Notice.category_id == category_id,
        Notice.title == new_notice.title,
        Notice.url == new_notice.url,
        Notice.expired_at == new_notice.expired_at,
    )
    return await fetch_one(select_query)


async def delete_notice(
    notice_category_id: int,
    notice_id: int,
) -> None:
    delete_query = delete(Notice).where(
        Notice.category_id == notice_category_id,
        Notice.id_ == notice_id,
    )
    await execute_query(delete_query)


async def update_notice(
    user_id: str,
    notice_category_id: int,
    notice_id: int,
    new_notice: UpdateNoticeRequest,
) -> Notice | None:
    update_data: dict[str, str | datetime.datetime] = {}
    if new_notice.title:
        update_data["title"] = new_notice.title
    if new_notice.url:
        update_data["url"] = new_notice.url
    if new_notice.expired_at:
        update_data["expired_at"] = new_notice.expired_at
    if new_notice.language:
        update_data["language"] = new_notice.language
    update_query = (
        update(Notice)
        .where(
            Notice.category_id == notice_category_id,
            Notice.id_ == notice_id,
        )
        .values(update_data)
    )
    await execute_query(update_query)
    select_query = select(Notice).where(
        Notice.category_id == notice_category_id,
        Notice.id_ == notice_id,
    )
    return await fetch_one(select_query)
