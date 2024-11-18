from sqlalchemy import select, insert, delete, update

from building.schemas import (
    CreateRoomRequest,
    CreateBuildingRequest,
    UpdateBuildingRequest,
    UpdateRoomRequest,
)
from database import fetch_all, fetch_one, execute_query
from model.building import Building, Room


async def list_building() -> list[Building]:
    select_query = select(Building)
    return await fetch_all(select_query)


async def list_building_filter(
    campus_id: int | None = None,
    name: str | None = None,
) -> list[Building]:
    conditions = []
    if campus_id is not None:
        conditions.append(Building.campus_id == campus_id)
    if name is not None:
        conditions.append(Building.name.like(f"%{name}%"))
    select_query = select(Building).where(*conditions)
    return await fetch_all(select_query)


async def get_building(building_name: str) -> Building | None:
    select_query = select(Building).where(Building.name == building_name)
    return await fetch_one(select_query)


async def create_building(
    new_building: CreateBuildingRequest,
) -> Building | None:
    insert_query = (
        insert(Building)
        .values(
            {
                "id": new_building.id_,
                "name": new_building.name,
                "campus_id": new_building.campus_id,
                "latitude": new_building.latitude,
                "longitude": new_building.longitude,
                "url": new_building.url,
            },
        )
    )
    await execute_query(insert_query)


async def update_building(
    building_name: str,
    new_building: UpdateBuildingRequest,
) -> Building | None:
    payload: dict[str, str | float] = {}
    if new_building.id_ is not None:
        payload["id_"] = new_building.id_
    if new_building.latitude is not None:
        payload["latitude"] = new_building.latitude
    if new_building.longitude is not None:
        payload["longitude"] = new_building.longitude
    if new_building.url is not None:
        payload["url"] = new_building.url
    update_query = (
        update(Building)
        .where(Building.name == building_name)
        .values(payload)
    )
    await execute_query(update_query)


async def delete_building(building_name: str) -> None:
    delete_query = delete(Building).where(Building.id_ == building_name)
    await execute_query(delete_query)


async def list_room_filter(
    building_name: str,
    name: str | None = None,
    number: str | None = None,
) -> list[Room]:
    conditions = [Room.building_name == building_name]
    if name is not None:
        conditions.append(Room.name.like(f"%{name}%"))
    if number is not None:
        conditions.append(Room.number == number)
    select_query = select(Room).where(*conditions)
    return await fetch_all(select_query)


async def get_room(
    building_name: str,
    room_number: str,
) -> Room | None:
    select_query = select(Room).where(
        Room.building_name == building_name,
        Room.number == room_number,
    )
    return await fetch_one(select_query)


async def create_room(
    building_name: str,
    new_room: CreateRoomRequest,
) -> Room | None:
    insert_query = (
        insert(Room)
        .values(
            {
                "building_name": building_name,
                "name": new_room.name,
                "number": new_room.number,
            },
        )
    )
    await execute_query(insert_query)


async def update_room(
    building_name: str,
    room_number: str,
    new_room: UpdateRoomRequest,
) -> Room | None:
    payload: dict[str, str] = {}
    if new_room.name is not None:
        payload["name"] = new_room.name
    if new_room.number is not None:
        payload["number"] = new_room.number

    update_query = (
        update(Room)
        .where(
            Room.building_name == building_name,
            Room.number == room_number,
        )
        .values(payload)
    )
    await execute_query(update_query)


async def delete_room(building_name: str, room_number: str) -> None:
    delete_query = delete(Room).where(
        Room.building_name == building_name,
        Room.number == room_number,
    )
    await execute_query(delete_query)
