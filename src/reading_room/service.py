from sqlalchemy import select, insert, update, delete

from database import fetch_all, fetch_one, execute_query
from model.reading_room import ReadingRoom
from reading_room.schemas import CreateReadingRoomRequest, UpdateReadingRoomRequest


async def list_reading_room() -> list[dict[str, str]]:
    select_query = select(ReadingRoom)
    return await fetch_all(select_query)


async def list_reading_room_filter(campus_id: int) -> list[dict[str, str]]:
    select_query = select(ReadingRoom).filter(
        ReadingRoom.campus_id == campus_id,
    )
    return await fetch_all(select_query)


async def create_reading_room(
    new_reading_room: CreateReadingRoomRequest,
) -> dict[str, str] | None:
    insert_query = (
        insert(ReadingRoom)
        .values(
            {
                "room_id": new_reading_room.id,
                "campus_id": new_reading_room.campus_id,
                "room_name": new_reading_room.name,
                "is_active": new_reading_room.active,
                "is_reservable": new_reading_room.reservable,
                "total": new_reading_room.total_seats,
                "active_total": new_reading_room.active_seats,
            },
        )
        .returning(ReadingRoom)
    )

    return await fetch_one(insert_query)


async def get_reading_room(reading_room_id: int) -> dict[str, str] | None:
    select_query = select(ReadingRoom).where(ReadingRoom.id == reading_room_id)
    return await fetch_one(select_query)


async def update_reading_room(
    room_id: int,
    new_reading_room: UpdateReadingRoomRequest,
) -> dict[str, str] | None:
    update_query = (
        update(ReadingRoom)
        .where(ReadingRoom.id == room_id)
        .values(
            {
                "is_active": new_reading_room.active,
                "is_reservable": new_reading_room.reservable,
                "total": new_reading_room.total_seats,
                "active_total": new_reading_room.active_seats,
            },
        )
        .returning(ReadingRoom)
    )

    return await fetch_one(update_query)


async def delete_reading_room(room_id: int) -> None:
    delete_query = delete(ReadingRoom).where(ReadingRoom.id == room_id)
    await execute_query(delete_query)
