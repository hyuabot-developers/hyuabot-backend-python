import datetime
from typing import Optional

import strawberry
from pytz import timezone
from sqlalchemy import select, or_
from sqlalchemy.orm import joinedload, load_only

from database import fetch_all
from model.notice import Notice, NoticeCategory


@strawberry.type
class NoticeCategoryQuery:
    id_: int = strawberry.field(description="Category ID", name="id")
    name: str = strawberry.field(description="Category name")


@strawberry.type
class NoticeQuery:
    category: NoticeCategoryQuery = strawberry.field(description="Category of notice")
    id_: int = strawberry.field(description="Notice ID", name="id")
    title: str = strawberry.field(description="Notice title")
    url: str = strawberry.field(description="Notice URL")
    expired_at: datetime.datetime | None = strawberry.field(description="Notice expired at")
    user_id: str = strawberry.field(description="User ID", name="userID")
    language: str = strawberry.field(description="Language")


async def resolve_notice(
    language: str,
    category_id: Optional[int] = None,
    title: Optional[str] = None,
) -> list[NoticeQuery]:
    now = datetime.datetime.now().astimezone(timezone("Asia/Seoul"))
    notice_conditions = [
        Notice.language == language,
        or_(Notice.expired_at > now, Notice.expired_at.is_(None)),
    ]
    if category_id is not None:
        notice_conditions.append(Notice.category_id == category_id)
    if title is not None:
        notice_conditions.append(Notice.title.like(f"%{title}%"))
    select_query = (
        select(Notice)
        .where(*notice_conditions)
        .order_by(Notice.id_)
        .options(
            joinedload(Notice.category).options(
                load_only(NoticeCategory.id_, NoticeCategory.name),
            ),
        )
    )
    notices: list[Notice] = await fetch_all(select_query)
    result: list[NoticeQuery] = []
    for notice in notices:
        result.append(
            NoticeQuery(
                category=NoticeCategoryQuery(
                    id_=notice.category.id_,
                    name=notice.category.name,
                ),
                id_=notice.id_,
                title=notice.title,
                url=notice.url,
                expired_at=notice.expired_at if notice.expired_at else None,
                user_id=notice.user_id,
                language=notice.language,
            ),
        )
    return result
