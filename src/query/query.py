import strawberry

from building.query import BuildingQuery, resolve_building, RoomQuery, resolve_room
from cafeteria.query import CafeteriaQuery, resolve_menu
from subway.query import StationQuery, resolve_subway


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
    menu: list[CafeteriaQuery] = strawberry.field(
        resolver=resolve_menu,
        description="Cafeteria query",
    )
    subway: list[StationQuery] = strawberry.field(
        resolver=resolve_subway,
        description="Subway query",
    )
