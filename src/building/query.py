from typing import Optional

import strawberry
from sqlalchemy import select

from database import fetch_all
from model.building import Building


@strawberry.type
class RoomQuery:
    name: str = strawberry.field(description="Room name")
    number: str = strawberry.field(description="Room number")


@strawberry.type
class BuildingQuery:
    _id: str = strawberry.field(description="Building ID", name="id")
    name: str = strawberry.field(description="Building name")
    latitude: float = strawberry.field(description="Building latitude")
    longitude: float = strawberry.field(description="Building longitude")
    url: Optional[str] = strawberry.field(description="Blog URL")
    rooms: list[RoomQuery] = strawberry.field(description="Rooms in the building")


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
    building_list = await fetch_all(select_query)
    return list(
        map(
            lambda building: BuildingQuery(
                _id=building["id"],
                name=building["name"],
                latitude=building["latitude"],
                longitude=building["longitude"],
                url=building["url"],
                rooms=list(
                    map(
                        lambda room: RoomQuery(
                            name=room["name"],
                            number=room["number"],
                        ),
                        building["rooms"],
                    ),
                ),
            ),
            building_list,
        ),
    )
