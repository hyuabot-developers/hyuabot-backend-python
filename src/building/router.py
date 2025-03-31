from typing import Callable

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
from model.building import Building, Room
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
    mapping_func: Callable[[Building], dict[str, str | int | float]] = lambda x: {
        "id": x.id_,
        "name": x.name,
        "campusID": x.campus_id,
        "latitude": x.latitude,
        "longitude": x.longitude,
        "url": x.url,
    }

    return {"data": map(mapping_func, data)}


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
        "id": building.id_,
        "name": building.name,
        "campusID": building.campus_id,
        "latitude": building.latitude,
        "longitude": building.longitude,
        "url": building.url,
    }


@router.get("/{building_name}", response_model=BuildingItemResponse)
async def get_building(
    building_name: str,
    _: str = Depends(parse_jwt_user_data),
):
    building = await service.get_building(building_name)
    if building is None:
        raise BuildingNotFound()
    return {
        "id": building.id_,
        "name": building.name,
        "campusID": building.campus_id,
        "latitude": building.latitude,
        "longitude": building.longitude,
        "url": building.url,
    }


@router.put("/{building_name}", response_model=BuildingItemResponse)
async def update_building(
    payload: UpdateBuildingRequest,
    building_name: str = Depends(get_valid_building),
    _: str = Depends(parse_jwt_user_data),
):
    building = await service.update_building(building_name, payload)
    if building is None:
        raise DetailedHTTPException()
    return {
        "id": building.id_,
        "name": building.name,
        "campusID": building.campus_id,
        "latitude": building.latitude,
        "longitude": building.longitude,
        "url": building.url,
    }


@router.delete("/{building_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_building(
    building_name: str = Depends(delete_valid_building),
    _: str = Depends(parse_jwt_user_data),
):
    await service.delete_building(building_name)
    return None


@router.get("/{building_name}/room", response_model=RoomListResponse)
async def get_building_room(
    name: str | None = None,
    number: str | None = None,
    building_name: str = Depends(get_valid_building),
    _: str = Depends(parse_jwt_user_data),
):
    if name is None and number is None:
        room_list = await service.list_room_filter(building_name)
    else:
        room_list = await service.list_room_filter(
            building_name,
            name,
            number,
        )
    mapping_func: Callable[[Room], dict[str, str]] = lambda x: {
        "buildingID": building_name,
        "name": x.name,
        "number": x.number,
    }
    return {"data": map(mapping_func, room_list)}


@router.post(
    "/{building_name}/room",
    response_model=RoomItemResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_building_room(
    new_room: CreateRoomRequest,
    building_name: str = Depends(get_valid_building),
    _: str = Depends(parse_jwt_user_data),
):
    new_room = await create_valid_room(building_name, new_room)
    room = await service.create_room(building_name, new_room)
    if room is None:
        raise DetailedHTTPException()
    return {
        "buildingID": building_name,
        "name": room.name,
        "number": room.number,
    }


@router.get("/{building_name}/room/{room_number}", response_model=RoomItemResponse)
async def get_building_room_item(
    room_number: str,
    building_name: str = Depends(get_valid_building),
    _: str = Depends(parse_jwt_user_data),
):
    room = await service.get_room(building_name, room_number)
    if room is None:
        raise RoomNotFound()
    return {
        "buildingID": building_name,
        "name": room.name,
        "number": room.number,
    }


@router.put("/{building_name}/room/{room_number}", response_model=RoomItemResponse)
async def update_building_room_item(
    payload: UpdateRoomRequest,
    building_name: str = Depends(get_valid_building),
    room_number: str = Depends(get_valid_room),
    _: str = Depends(parse_jwt_user_data),
):
    room = await service.update_room(building_name, room_number, payload)
    if room is None:
        raise DetailedHTTPException()
    return {
        "buildingID": building_name,
        "name": room.name,
        "number": room.number,
    }


@router.delete(
    "/{building_name}/room/{room_number}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_building_room_item(
    room_number: str = Depends(get_valid_room),
    building_name: str = Depends(get_valid_building),
    _: str = Depends(parse_jwt_user_data),
):
    await service.delete_room(building_name, room_number)
    return None
