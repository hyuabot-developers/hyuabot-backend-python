from fastapi import APIRouter, Depends
from starlette import status

from notice import service
from notice.dependancies import (
    create_valid_category,
    get_valid_category,
    create_valid_notice,
    get_valid_notice,
)
from notice.exceptions import (
    CategoryNotFound,
    NoticeNotFound,
)
from notice.schemas import (
    NoticeListResponse,
    NoticeDetailResponse,
    CreateNoticeCategoryRequest,
    CreateNoticeReqeust,
    UpdateNoticeRequest,
    NoticeCategoryListResponse,
    NoticeCategoryDetailResponse,
)
from exceptions import DetailedHTTPException
from user.jwt import parse_jwt_user_data

router = APIRouter()


@router.get("", response_model=NoticeCategoryListResponse)
async def get_notice_category_list(
    _: str = Depends(parse_jwt_user_data),
    name: str | None = None,
):
    if name is None:
        data = await service.list_notice_category()
    else:
        data = await service.list_notice_category_filter(name)
    return {
        "data": map(
            lambda x: {
                "id": x["category_id"],
                "name": x["category_name"],
            },
            data,
        ),
    }


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=NoticeCategoryDetailResponse,
)
async def create_notice_category(
    new_category: CreateNoticeCategoryRequest = Depends(create_valid_category),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.create_notice_category(new_category)
    if data is None:
        raise DetailedHTTPException()
    return {
        "id": data["category_id"],
        "name": data["category_name"],
    }


@router.get("/{notice_category_id}", response_model=NoticeCategoryDetailResponse)
async def get_notice_category(
    notice_category_id: int,
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.get_notice_category(notice_category_id)
    if data is None:
        raise CategoryNotFound()
    return {
        "id": data["category_id"],
        "name": data["category_name"],
    }


@router.delete(
    "/{notice_category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_notice_category(
    _: str = Depends(parse_jwt_user_data),
    notice_category_id: int = Depends(get_valid_category),
):
    await service.delete_notice_category(notice_category_id)


@router.get("/{notice_category_id}/notices", response_model=NoticeListResponse)
async def get_notice_list(
    notice_category_id: int = Depends(get_valid_category),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.get_notice_list(notice_category_id)
    return {
        "data": map(
            lambda x: {
                "userID": x["user_id"],
                "id": x["notice_id"],
                "title": x["title"],
                "url": x["url"],
                "expiredAt": x["expired_at"],
            },
            data,
        ),
    }


@router.get(
    "/{notice_category_id}/notices/{notice_id}",
    response_model=NoticeDetailResponse,
)
async def get_notice(
    notice_id: int,
    notice_category_id: int = Depends(get_valid_category),
    _: str = Depends(parse_jwt_user_data),
):
    data = await service.get_notice(notice_category_id, notice_id)
    if data is None:
        raise NoticeNotFound()
    return {
        "userID": data["user_id"],
        "id": data["notice_id"],
        "title": data["title"],
        "url": data["url"],
        "expiredAt": data["expired_at"],
    }


@router.post(
    "/{notice_category_id}/notices",
    status_code=status.HTTP_201_CREATED,
    response_model=NoticeDetailResponse,
)
async def create_notice(
    new_notice: CreateNoticeReqeust = Depends(create_valid_notice),
    notice_category_id: int = Depends(get_valid_category),
    user_id: str = Depends(parse_jwt_user_data),
):
    data = await service.create_notice(
        user_id,
        notice_category_id,
        new_notice,
    )
    if data is None:
        raise DetailedHTTPException()
    return {
        "userID": data["user_id"],
        "id": data["notice_id"],
        "title": data["title"],
        "url": data["url"],
        "expiredAt": data["expired_at"],
    }


@router.patch(
    "/{notice_category_id}/notices/{notice_id}",
    response_model=NoticeDetailResponse,
)
async def update_notice(
    new_notice: UpdateNoticeRequest,
    notice_category_id: int = Depends(get_valid_category),
    notice_id: int = Depends(get_valid_notice),
    user_id: str = Depends(parse_jwt_user_data),
):
    data = await service.update_notice(
        user_id,
        notice_category_id,
        notice_id,
        new_notice,
    )
    if data is None:
        raise DetailedHTTPException()
    return {
        "userID": data["user_id"],
        "id": data["notice_id"],
        "title": data["title"],
        "url": data["url"],
        "expiredAt": data["expired_at"],
    }


@router.delete(
    "/{notice_category_id}/notices/{notice_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_notice(
    notice_id: int,
    notice_category_id: int = Depends(get_valid_category),
    _: str = Depends(parse_jwt_user_data),
):
    await service.delete_notice(notice_category_id, notice_id)
