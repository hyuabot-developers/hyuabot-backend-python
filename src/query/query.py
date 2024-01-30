import strawberry

from building.query import BuildingQuery, resolve_building, RoomQuery, resolve_room


@strawberry.type
class Query:
    health: bool = strawberry.field(
        resolver=lambda: True,
        description="Health check",
    )
    building: list[BuildingQuery] = strawberry.field(
        resolver=resolve_building,
        description="Building query",
    )
    room: list[RoomQuery] = strawberry.field(
        resolver=resolve_room,
        description="Room query",
    )
