from exceptions import Conflict, NotFound, BadRequest


class DuplicateBuildingID(Conflict):
    DETAIL = "DUPLICATE_BUILDING_ID"


class BuildingNotFound(NotFound):
    DETAIL = "BUILDING_NOT_FOUND"


class BuildingHasRoom(BadRequest):
    DETAIL = "BUILDING_HAS_ROOM"


class DuplicateRoomID(Conflict):
    DETAIL = "DUPLICATE_ROOM_ID"


class RoomNotFound(NotFound):
    DETAIL = "ROOM_NOT_FOUND"
