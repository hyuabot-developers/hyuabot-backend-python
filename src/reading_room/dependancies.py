from reading_room import service
from reading_room.exceptions import DuplicateReadingRoomID, ReadingRoomNotFound
from reading_room.schemas import CreateReadingRoomRequest


async def create_valid_reading_room(
    new_reading_room: CreateReadingRoomRequest,
) -> CreateReadingRoomRequest:
    if await service.get_reading_room(new_reading_room.id):
        raise DuplicateReadingRoomID()

    return new_reading_room


async def get_valid_reading_room(reading_room_id: int) -> int:
    if await service.get_reading_room(reading_room_id) is None:
        raise ReadingRoomNotFound()

    return reading_room_id
