from campus import service
from campus.exceptions import DuplicateCampusID, CampusNotFound
from campus.schemas import CreateCampusRequest


async def create_valid_campus(
    new_campus: CreateCampusRequest,
) -> CreateCampusRequest:
    if await service.get_campus(new_campus.id):
        raise DuplicateCampusID()

    return new_campus


async def get_valid_campus(campus_id: int) -> int:
    if await service.get_campus(campus_id) is None:
        raise CampusNotFound()

    return campus_id
