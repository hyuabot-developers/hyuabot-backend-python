import strawberry

from building.query import BuildingQuery, resolve_building, RoomQuery, resolve_room
from bus.query import StopQuery, resolve_bus
from cafeteria.query import CafeteriaQuery, resolve_menu
from notice.query import NoticeQuery, resolve_notice
from shuttle.query import ShuttleQuery, resolve_shuttle
from subway.query import StationQuery, resolve_subway
from reading_room.query import ReadingRoomQuery, resolve_reading_room


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
    reading_room: list[ReadingRoomQuery] = strawberry.field(
        resolver=resolve_reading_room,
        description="Reading room query",
        name="readingRoom",
    )
    subway: list[StationQuery] = strawberry.field(
        resolver=resolve_subway,
        description="Subway query",
    )
    bus: list[StopQuery] = strawberry.field(
        resolver=resolve_bus,
        description="Bus stop query",
    )
    shuttle: ShuttleQuery = strawberry.field(
        resolver=resolve_shuttle,
        description="Shuttle query",
    )
    notice: list[NoticeQuery] = strawberry.field(
        resolver=resolve_notice,
        description="Notice query",
    )
