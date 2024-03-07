from typing import Optional, Callable

import strawberry
from sqlalchemy import true, select, false

from database import fetch_all
from model.reading_room import ReadingRoom


@strawberry.type
class ReadingRoomQuery:
    id_: int = strawberry.field(
        description="Reading room ID",
        name="id",
    )
    name: str = strawberry.field(description="Reading room name")
    is_active: bool = strawberry.field(
        description="Is reading room active",
        name="isActive",
    )
    total: int = strawberry.field(description="Total seats in reading room")
    active: int = strawberry.field(
        description="Active seats in reading room",
        name="active",
    )
    occupied: int = strawberry.field(
        description="Occupied seats in reading room",
        name="occupied",
    )
    available: int = strawberry.field(
        description="Available seats in reading room",
        name="available",
    )
    updated_at: str = strawberry.field(
        description="Last updated time",
        name="updatedAt",
    )


async def resolve_reading_room(
    campus_id: Optional[int] = None,
    name: Optional[str] = None,
    is_active: Optional[bool] = None,
) -> list[ReadingRoomQuery]:
    room_conditions = []
    if campus_id:
        room_conditions.append(ReadingRoom.campus_id == campus_id)
    if name:
        room_conditions.append(ReadingRoom.name.like(f"%{name}%"))
    if is_active is None or is_active is True:
        room_conditions.append(ReadingRoom.active.is_(true()))
    else:
        room_conditions.append(ReadingRoom.active.is_(false()))
    room_select_query = (
        select(ReadingRoom).filter(*room_conditions).order_by(ReadingRoom.name)
    )
    room_list = await fetch_all(room_select_query)
    reading_room_mapping_func: Callable[[ReadingRoom], ReadingRoomQuery] = (
        lambda room: ReadingRoomQuery(
            id_=room.id_,
            name=room.name,
            is_active=room.active,
            total=room.total_seats,
            active=room.active_total_seats,
            occupied=room.occupied_seats,
            available=room.available_seats,
            updated_at=room.updated_at.isoformat(),
        )
    )
    return list(map(reading_room_mapping_func, room_list))
