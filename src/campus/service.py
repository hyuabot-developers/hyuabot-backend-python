from sqlalchemy import select, delete, insert, update

from campus.schemas import CreateCampusRequest, UpdateCampusRequest
from database import fetch_one, fetch_all, execute_query
from model.campus import Campus


async def get_campus(campus_id: int) -> Campus | None:
    select_query = select(Campus).where(Campus.id_ == campus_id)
    return await fetch_one(select_query)


async def list_campus() -> list[Campus]:
    select_query = select(Campus)
    return await fetch_all(select_query)


async def list_campus_filter(campus_name: str) -> list[Campus]:
    select_query = select(Campus).filter(
        Campus.name.like(f"%{campus_name}%"),
    )
    return await fetch_all(select_query)


async def update_campus(
    campus_id: int,
    new_campus: UpdateCampusRequest,
) -> Campus | None:
    update_query = (
        update(Campus)
        .where(Campus.id_ == campus_id)
        .values(
            {
                "name": new_campus.name,
            },
        )
    )
    await execute_query(update_query)
    select_query = select(Campus).where(Campus.id_ == campus_id)
    return await fetch_one(select_query)


async def delete_campus(campus_id: int) -> None:
    delete_query = delete(Campus).where(Campus.id_ == campus_id)
    await execute_query(delete_query)


async def create_campus(
    new_campus: CreateCampusRequest,
) -> Campus | None:
    insert_query = (
        insert(Campus)
        .values(
            {
                "campus_id": new_campus.id_,
                "campus_name": new_campus.name,
            },
        )
    )
    await execute_query(insert_query)
    select_query = select(Campus).where(Campus.id_ == new_campus.id_)
    return await fetch_one(select_query)
