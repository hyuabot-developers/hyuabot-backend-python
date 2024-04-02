import datetime
from typing import Optional

import strawberry
from sqlalchemy import select
from sqlalchemy.orm import joinedload, load_only

from database import fetch_all
from model.calendar import Calendar, CalendarVersion
from model.notice import NoticeCategory


@strawberry.type
class CalendarCategoryQuery:
    id_: int = strawberry.field(description="Category ID", name="id")
    name: str = strawberry.field(description="Category name")


@strawberry.type
class EventQuery:
    category: CalendarCategoryQuery = strawberry.field(
        description="Category of event",
    )
    id_: int = strawberry.field(description="Calendar ID", name="id")
    title: str = strawberry.field(description="Calendar title")
    description: str = strawberry.field(description="Calendar description")
    start_date: datetime.date = strawberry.field(
        description="Calendar start date", name="start",
    )
    end_date: datetime.date = strawberry.field(
        description="Calendar end date", name="end",
    )


@strawberry.type
class CalendarQuery:
    version: str = strawberry.field(description="Version of event")
    data: list[EventQuery] = strawberry.field(description="List of events")


async def resolve_events(
    category_id: Optional[int] = None,
    title: Optional[str] = None,
) -> list[EventQuery]:
    calendar_conditions = []
    if category_id is not None:
        calendar_conditions.append(Calendar.category_id == category_id)
    if title is not None:
        calendar_conditions.append(Calendar.title.like(f"%{title}%"))
    select_query = (
        select(Calendar)
        .where(*calendar_conditions)
        .order_by(Calendar.id_)
        .options(
            joinedload(Calendar.category).options(
                load_only(NoticeCategory.id_, NoticeCategory.name),
            ),
        )
    )
    events: list[Calendar] = await fetch_all(select_query)
    result: list[EventQuery] = []
    for event in events:
        result.append(
            EventQuery(
                category=CalendarCategoryQuery(
                    id_=event.category.id_,
                    name=event.category.name,
                ),
                id_=event.id_,
                title=event.title,
                description=event.description,
                start_date=event.start_date,
                end_date=event.end_date,
            ),
        )
    return result


async def resolve_calendars(
    category_id: Optional[int] = None,
    title: Optional[str] = None,
) -> CalendarQuery:
    version_select_statement = select(CalendarVersion).order_by(
        CalendarVersion.created_at.desc(),
    ).limit(1)
    version = (await fetch_all(version_select_statement))[0].name
    events = await resolve_events(category_id, title)
    return CalendarQuery(version=version, data=events)
