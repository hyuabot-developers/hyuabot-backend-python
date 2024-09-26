from typing import Optional

import strawberry
from sqlalchemy import select
from sqlalchemy.orm import joinedload, load_only

from database import fetch_all
from model.contact import PhoneBook, PhoneBookVersion, PhoneBookCategory


@strawberry.type
class ContactCategoryQuery:
    id_: int = strawberry.field(description="Category ID", name="id")
    name: str = strawberry.field(description="Category name")


@strawberry.type
class ContactItemQuery:
    category: ContactCategoryQuery = strawberry.field(
        description="Category of contact",
    )
    id_: int = strawberry.field(description="Contact ID", name="id")
    name: str = strawberry.field(description="Contact name")
    phone: str = strawberry.field(description="Contact phone number")
    campusID: int = strawberry.field(description="Campus ID")


@strawberry.type
class ContactQuery:
    version: str = strawberry.field(description="Version of event")
    data: list[ContactItemQuery] = strawberry.field(description="List of events")


async def resolve_contacts(
    campus_id: Optional[int] = None,
    category_id: Optional[int] = None,
    name: Optional[str] = None,
) -> list[ContactItemQuery]:
    contact_conditions = []
    if category_id is not None:
        contact_conditions.append(PhoneBook.category_id == category_id)
    if name is not None:
        contact_conditions.append(PhoneBook.name.like(f"%{name}%"))
    if campus_id is not None:
        contact_conditions.append(PhoneBook.campus_id == campus_id)
    select_query = (
        select(PhoneBook)
        .where(*contact_conditions)
        .order_by(PhoneBook.id_)
        .options(
            joinedload(PhoneBook.category).options(
                load_only(PhoneBookCategory.id_, PhoneBookCategory.name),
            ),
        )
    )
    contacts: list[PhoneBook] = await fetch_all(select_query)
    result: list[ContactItemQuery] = []
    for contact in contacts:
        result.append(
            ContactItemQuery(
                category=ContactCategoryQuery(
                    id_=contact.category.id_,
                    name=contact.category.name,
                ),
                id_=contact.id_,
                name=contact.name,
                phone=contact.phone,
                campusID=contact.campus_id,
            ),
        )
    return result


async def resolve_contact(
    campus_id: Optional[int] = None,
    category_id: Optional[int] = None,
    name: Optional[str] = None,
) -> ContactQuery:
    version_select_statement = (
        select(PhoneBookVersion)
        .order_by(
            PhoneBookVersion.created_at.desc(),
        )
        .limit(1)
    )
    version = (await fetch_all(version_select_statement))[0].name
    events = await resolve_contacts(campus_id, category_id, name)
    return ContactQuery(version=version, data=events)
