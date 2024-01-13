from building import service
from building.exceptions import (
    DuplicateBuildingID,
    BuildingNotFound,
    BuildingHasRoom,
    DuplicateRoomID,
    RoomNotFound,
)
from building.schemas import (
    CreateBuildingRequest,
    CreateRoomRequest,
)


async def create_valid_building(
    new_building: CreateBuildingRequest,
) -> CreateBuildingRequest:
    if await service.get_building(new_building.id):
        raise DuplicateBuildingID()
    return new_building


async def get_valid_building(building_id: str) -> str:
    if await service.get_building(building_id) is None:
        raise BuildingNotFound()
    return building_id


async def delete_valid_building(building_id: str) -> str:
    if await service.get_building(building_id) is None:
        raise BuildingNotFound()
    elif await service.list_room_filter(building_id):
        raise BuildingHasRoom()
    return building_id


async def create_valid_room(new_room: CreateRoomRequest) -> CreateRoomRequest:
    if await service.get_room(new_room.building_id, new_room.number):
        raise DuplicateRoomID()
    return new_room


async def get_valid_room(building_id: str, room_number: str) -> str:
    if await service.get_room(building_id, room_number) is None:
        raise RoomNotFound()
    return room_number
