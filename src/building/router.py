from fastapi import APIRouter, Depends
from starlette import status

from building import service
from building.dependencies import (
    create_valid_building,
    delete_valid_building,
    get_valid_building,
    create_valid_room,
    get_valid_room,
)
from building.exceptions import BuildingNotFound, RoomNotFound
from building.schemas import (
    BuildingListResponse,
    CreateBuildingRequest,
    BuildingItemResponse,
    UpdateBuildingRequest,
    RoomListResponse,
    CreateRoomRequest,
    RoomItemResponse,
    UpdateRoomRequest,
)
from exceptions import DetailedHTTPException
from user.jwt import parse_jwt_user_data

router = APIRouter()


@router.get("", response_model=BuildingListResponse)
async def get_building_list(
    campus: int | None = None,
    name: str | None = None,
    _: str = Depends(parse_jwt_user_data),
):
    if campus is None and name is None:
        data = await service.list_building()
    else:
        data = await service.list_building_filter(campus, name)

    return {
        "data": map(
            lambda x: {
                "id": x["id"],
                "name": x["name"],
                "campusID": x["campus_id"],
                "latitude": x["latitude"],
                "longitude": x["longitude"],
                "url": x["url"],
            },
            data,
        ),
    }


@router.post(
    "",
    response_model=BuildingItemResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_building(
    new_building: CreateBuildingRequest = Depends(create_valid_building),
    _: str = Depends(parse_jwt_user_data),
):
    building = await service.create_building(new_building)
    if building is None:
        raise DetailedHTTPException()
    return {
        "id": building["id"],
        "name": building["name"],
        "campusID": building["campus_id"],
        "latitude": building["latitude"],
        "longitude": building["longitude"],
        "url": building["url"],
    }


@router.get("/{building_id}", response_model=BuildingItemResponse)
async def get_building(
    building_id: str,
    _: str = Depends(parse_jwt_user_data),
):
    building = await service.get_building(building_id)
    if building is None:
        raise BuildingNotFound()
    return {
        "id": building["id"],
        "name": building["name"],
        "campusID": building["campus_id"],
        "latitude": building["latitude"],
        "longitude": building["longitude"],
        "url": building["url"],
    }


@router.patch("/{building_id}", response_model=BuildingItemResponse)
async def update_building(
    payload: UpdateBuildingRequest,
    building_id: str = Depends(get_valid_building),
    _: str = Depends(parse_jwt_user_data),
):
    building = await service.update_building(building_id, payload)
    if building is None:
        raise DetailedHTTPException()
    return {
        "id": building["id"],
        "name": building["name"],
        "campusID": building["campus_id"],
        "latitude": building["latitude"],
        "longitude": building["longitude"],
        "url": building["url"],
    }


@router.delete("/{building_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_building(
    building_id: str = Depends(delete_valid_building),
    _: str = Depends(parse_jwt_user_data),
):
    await service.delete_building(building_id)
    return None


@router.get("/{building_id}/room", response_model=RoomListResponse)
async def get_building_room(
    name: str | None = None,
    floor: str | None = None,
    number: str | None = None,
    building_id: str = Depends(get_valid_building),
    _: str = Depends(parse_jwt_user_data),
):
    if name is None and floor is None and number is None:
        room_list = await service.list_room_filter(building_id)
    else:
        room_list = await service.list_room_filter(
            building_id,
            name,
            floor,
            number,
        )
    return {
        "data": map(
            lambda x: {
                "id": x["id"],
                "buildingID": x["building_id"],
                "name": x["name"],
                "floor": x["floor"],
                "number": x["number"],
            },
            room_list,
        ),
    }


@router.post(
    "/{building_id}/room",
    response_model=RoomItemResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_building_room(
    new_room: CreateRoomRequest = Depends(create_valid_room),
    building_id: str = Depends(get_valid_building),
    _: str = Depends(parse_jwt_user_data),
):
    room = await service.create_room(building_id, new_room)
    if room is None:
        raise DetailedHTTPException()
    return {
        "id": room["id"],
        "buildingID": room["building_id"],
        "name": room["name"],
        "floor": room["floor"],
        "number": room["number"],
    }


@router.get("/{building_id}/room/{room_id}", response_model=RoomItemResponse)
async def get_building_room_item(
    room_id: int,
    building_id: str = Depends(get_valid_building),
    _: str = Depends(parse_jwt_user_data),
):
    room = await service.get_room(room_id)
    if room is None:
        raise RoomNotFound()
    return {
        "id": room["id"],
        "buildingID": building_id,
        "name": room["name"],
        "floor": room["floor"],
        "number": room["number"],
    }


@router.patch("/{building_id}/room/{room_id}", response_model=RoomItemResponse)
async def update_building_room_item(
    payload: UpdateRoomRequest,
    building_id: str = Depends(get_valid_building),
    room_id: int = Depends(get_valid_room),
    _: str = Depends(parse_jwt_user_data),
):
    room = await service.update_room(building_id, room_id, payload)
    if room is None:
        raise DetailedHTTPException()
    return {
        "id": room["id"],
        "buildingID": room["building_id"],
        "name": room["name"],
        "floor": room["floor"],
        "number": room["number"],
    }


@router.delete("/{building_id}/room/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_building_room_item(
    room_id: int = Depends(get_valid_room),
    building_id: str = Depends(get_valid_building),
    _: str = Depends(parse_jwt_user_data),
):
    await service.delete_room(building_id, room_id)
    return None
