from typing import Optional, Callable

import strawberry
from sqlalchemy import select
from sqlalchemy.orm import joinedload, load_only

from database import fetch_all
from model.building import Building, Room


@strawberry.type
class RoomQuery:
    name: str = strawberry.field(description="Room name")
    number: str = strawberry.field(description="Room number")
    building_name: str = strawberry.field(
        description="Building name",
        name="buildingName",
    )
    latitude: float = strawberry.field(description="Building latitude")
    longitude: float = strawberry.field(description="Building longitude")


@strawberry.type
class BuildingQuery:
    _id: str = strawberry.field(description="Building ID", name="id")
    name: str = strawberry.field(description="Building name")
    latitude: float = strawberry.field(description="Building latitude")
    longitude: float = strawberry.field(description="Building longitude")
    url: Optional[str] = strawberry.field(description="Blog URL")


async def resolve_building(
    north: Optional[float] = None,
    south: Optional[float] = None,
    east: Optional[float] = None,
    west: Optional[float] = None,
    name: Optional[str] = None,
) -> list[BuildingQuery]:
    conditions = []
    if north is not None:
        conditions.append(Building.latitude < north)
    if south is not None:
        conditions.append(Building.latitude > south)
    if east is not None:
        conditions.append(Building.longitude < east)
    if west is not None:
        conditions.append(Building.longitude > west)
    if name is not None:
        conditions.append(Building.name.like(f"%{name}%"))
    select_query = select(Building).where(*conditions)
    building_list: list[Building] = await fetch_all(select_query)
    mapping_func: Callable[[Building], BuildingQuery] = lambda building: BuildingQuery(
        _id=building.id_,
        name=building.name,
        latitude=building.latitude,
        longitude=building.longitude,
        url=building.url,
    )
    return list(map(mapping_func, building_list))


async def resolve_room(
    building_name: Optional[str] = None,
    name: Optional[str] = None,
    number: Optional[str] = None,
) -> list[RoomQuery]:
    conditions = []
    if building_name is not None:
        conditions.append(Room.building_name.like(f"%{building_name}%"))
    if name is not None:
        conditions.append(Room.name.like(f"%{name}%"))
    if number is not None:
        conditions.append(Room.number.like(f"%{number}%"))
    select_query = (
        select(Room)
        .where(*conditions)
        .options(
            joinedload(Room.building).options(
                load_only(Building.name, Building.latitude, Building.longitude),
            ),
        )
    )
    room_list: list[Room] = await fetch_all(select_query)
    mapping_func: Callable[[Room], RoomQuery] = lambda room: RoomQuery(
        name=room.name,
        number=room.number,
        latitude=room.building.latitude,
        longitude=room.building.longitude,
        building_name=room.building.name,
    )
    return list(map(mapping_func, room_list))
