from typing import Any

from sqlalchemy import select, insert, delete, update

from building.schemas import (
    CreateRoomRequest,
    CreateBuildingRequest,
    UpdateBuildingRequest,
)
from database import fetch_all, fetch_one, execute_query
from model.building import Building, Room


async def list_building() -> list[dict[str, Any]]:
    select_query = select(Building)
    return await fetch_all(select_query)


async def list_building_filter(
    campus_id: int | None = None,
    name: str | None = None,
) -> list[dict[str, Any]]:
    conditions = []
    if campus_id is not None:
        conditions.append(Building.campus_id == campus_id)
    if name is not None:
        conditions.append(Building.name.like(f"%{name}%"))
    select_query = select(Building).where(*conditions)
    return await fetch_all(select_query)


async def get_building(building_id: str) -> dict[str, Any] | None:
    select_query = select(Building).where(Building.id == building_id)
    return await fetch_one(select_query)


async def create_building(
    new_building: CreateBuildingRequest,
) -> dict[str, Any] | None:
    insert_query = (
        insert(Building)
        .values(
            {
                "id": new_building.id,
                "name": new_building.name,
                "campus_id": new_building.campus_id,
                "latitude": new_building.latitude,
                "longitude": new_building.longitude,
                "url": new_building.url,
            },
        )
        .returning(Building)
    )
    return await fetch_one(insert_query)


async def update_building(
    building_id: str,
    new_building: UpdateBuildingRequest,
) -> dict[str, Any] | None:
    update_query = (
        update(Building)
        .where(Building.id == building_id)
        .values(
            {
                "name": new_building.name,
                "latitude": new_building.latitude,
                "longitude": new_building.longitude,
                "url": new_building.url,
            },
        )
        .returning(Building)
    )
    return await fetch_one(update_query)


async def delete_building(building_id: str) -> None:
    delete_query = delete(Building).where(Building.id == building_id)
    await execute_query(delete_query)


async def list_room_filter(
    building_id: str,
    name: str | None = None,
    floor: str | None = None,
    number: str | None = None,
) -> list[dict[str, Any]]:
    conditions = [Room.building_id == building_id]
    if name is not None:
        conditions.append(Room.name.like(f"%{name}%"))
    if floor is not None:
        conditions.append(Room.floor == floor)
    if number is not None:
        conditions.append(Room.number == number)
    select_query = select(Room).where(*conditions)
    return await fetch_all(select_query)


async def get_room(building_id: str, room_id: int) -> dict[str, Any] | None:
    select_query = select(Room).where(
        Room.building_id == building_id,
        Room.id == room_id,
    )
    return await fetch_one(select_query)


async def create_room(
    building_id: str,
    new_room: CreateRoomRequest,
) -> dict[str, Any] | None:
    insert_query = (
        insert(Room)
        .values(
            {
                "id": new_room.id,
                "building_id": building_id,
                "name": new_room.name,
                "floor": new_room.floor,
                "number": new_room.number,
            },
        )
        .returning(Room)
    )
    return await fetch_one(insert_query)


async def delete_room(building_id: str, room_id: int) -> None:
    delete_query = delete(Room).where(
        Room.building_id == building_id,
        Room.id == room_id,
    )
    await execute_query(delete_query)
