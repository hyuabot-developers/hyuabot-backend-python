from fastapi import APIRouter, Depends
from starlette import status

from reading_room import service
from reading_room.dependancies import (
    create_valid_reading_room,
    get_valid_reading_room,
)
from reading_room.exceptions import ReadingRoomNotFound
from reading_room.schemas import (
    ReadingRoomListResponse,
    ReadingRoomDetailResponse,
    CreateReadingRoomRequest,
    UpdateReadingRoomRequest,
)
from exceptions import DetailedHTTPException
from user.jwt import parse_jwt_user_data

router = APIRouter()


@router.get("", response_model=ReadingRoomListResponse)
async def get_reading_room_list(
    _: str = Depends(parse_jwt_user_data),
    campus: int | None = None,
):
    if campus is None:
        data = await service.list_reading_room()
    else:
        data = await service.list_reading_room_filter(campus)
    return {
        "data": map(
            lambda x: {
                "id": x["room_id"],
                "name": x["room_name"],
            },
            data,
        ),
    }


@router.get("/{reading_room_id}", response_model=ReadingRoomDetailResponse)
async def get_reading_room(
    reading_room_id: int,
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.get_reading_room(reading_room_id)
    if data is None:
        raise ReadingRoomNotFound()
    return {
        "id": data["room_id"],
        "name": data["room_name"],
        "total": data["total"],
        "active": data["active_total"],
        "available": data["available"],
        "updatedAt": data["last_updated_time"],
        "occupied": data["occupied"],
    }


@router.delete(
    "/{reading_room_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_reading_room(
    _: str = Depends(parse_jwt_user_data),
    reading_room_id: int = Depends(get_valid_reading_room),
):
    await service.delete_reading_room(reading_room_id)
    return None


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ReadingRoomDetailResponse,
)
async def create_reading_room(
    _: str = Depends(parse_jwt_user_data),
    new_reading_room: CreateReadingRoomRequest = Depends(create_valid_reading_room),
):
    reading_room = await service.create_reading_room(new_reading_room)
    if reading_room is None:
        raise DetailedHTTPException()
    return {
        "id": reading_room["room_id"],
        "name": reading_room["room_name"],
        "total": reading_room["total"],
        "active": reading_room["active_total"],
        "available": reading_room["available"],
        "updatedAt": reading_room["last_updated_time"],
        "occupied": reading_room["occupied"],
    }


@router.patch(
    "/{reading_room_id}",
    response_model=ReadingRoomDetailResponse,
)
async def update_reading_room(
    payload: UpdateReadingRoomRequest,
    _: str = Depends(parse_jwt_user_data),
    reading_room_id: int = Depends(get_valid_reading_room),
):
    reading_room = await service.update_reading_room(reading_room_id, payload)
    if reading_room is None:
        raise DetailedHTTPException()
    return {
        "id": reading_room["room_id"],
        "name": reading_room["room_name"],
        "total": reading_room["total"],
        "active": reading_room["active_total"],
        "available": reading_room["available"],
        "updatedAt": reading_room["last_updated_time"],
        "occupied": reading_room["occupied"],
    }
