from typing import Callable

from fastapi import APIRouter, Depends
from starlette import status

from campus import service
from campus.dependancies import create_valid_campus, get_valid_campus
from campus.exceptions import CampusNotFound
from campus.schemas import (
    CampusListResponse,
    CampusDetailResponse,
    CreateCampusRequest,
    UpdateCampusRequest,
)
from exceptions import DetailedHTTPException
from model.campus import Campus
from user.jwt import parse_jwt_user_data

router = APIRouter()


@router.get("", response_model=CampusListResponse)
async def get_campus_list(
    _: str = Depends(parse_jwt_user_data),
    name: str | None = None,
):
    if name is None:
        data = await service.list_campus()
    else:
        data = await service.list_campus_filter(name)
    mapping_func: Callable[[Campus], dict[str, int | str]] = lambda x: {
        "id": x.id_,
        "name": x.name,
    }
    return {"data": map(mapping_func, data)}


@router.get("/{campus_id}", response_model=CampusDetailResponse)
async def get_campus(
    campus_id: int,
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.get_campus(campus_id)
    if data is None:
        raise CampusNotFound()
    return {
        "id": data.id_,
        "name": data.name,
    }


@router.delete(
    "/{campus_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_campus(
    _: str = Depends(parse_jwt_user_data),
    campus_id: int = Depends(get_valid_campus),
):
    await service.delete_campus(campus_id)
    return None


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=CampusDetailResponse,
)
async def create_campus(
    _: str = Depends(parse_jwt_user_data),
    new_campus: CreateCampusRequest = Depends(create_valid_campus),
):
    data = await service.create_campus(new_campus)
    if data is None:
        raise DetailedHTTPException()
    return {
        "id": data.id_,
        "name": data.name,
    }


@router.put(
    "/{campus_id}",
    response_model=CampusDetailResponse,
)
async def update_campus(
    payload: UpdateCampusRequest,
    _: str = Depends(parse_jwt_user_data),
    campus_id: int = Depends(get_valid_campus),
):
    data = await service.update_campus(campus_id, payload)
    if data is None:
        raise DetailedHTTPException()
    return {
        "id": data.id_,
        "name": data.name,
    }
