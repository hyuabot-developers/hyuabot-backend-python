from sqlalchemy import select, delete, insert, update

from campus.schemas import CreateCampusRequest, UpdateCampusRequest
from database import fetch_one, fetch_all, execute_query
from model.campus import Campus


async def get_campus(campus_id: int) -> dict[str, str] | None:
    select_query = select(Campus).where(Campus.id == campus_id)
    return await fetch_one(select_query)


async def list_campus() -> list[dict[str, str]]:
    select_query = select(Campus)
    return await fetch_all(select_query)


async def list_campus_filter(campus_name: str) -> list[dict[str, str]]:
    select_query = select(Campus).filter(
        Campus.name.like(f"%{campus_name}%"),
    )
    return await fetch_all(select_query)


async def update_campus(
    campus_id: int,
    new_campus: UpdateCampusRequest,
) -> dict[str, str] | None:
    update_query = (
        update(Campus)
        .where(Campus.id == campus_id)
        .values(
            {
                "campus_name": new_campus.name,
            },
        )
        .returning(Campus)
    )

    return await fetch_one(update_query)


async def delete_campus(campus_id: int) -> None:
    delete_query = delete(Campus).where(Campus.id == campus_id)
    await execute_query(delete_query)


async def create_campus(
    new_campus: CreateCampusRequest,
) -> dict[str, str] | None:
    insert_query = (
        insert(Campus)
        .values(
            {
                "campus_id": new_campus.id,
                "campus_name": new_campus.name,
            },
        )
        .returning(Campus)
    )

    return await fetch_one(insert_query)
