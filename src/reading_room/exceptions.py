from exceptions import Conflict, NotFound


class DuplicateReadingRoomID(Conflict):
    DETAIL = "DUPLICATE_ROOM_ID"


class ReadingRoomNotFound(NotFound):
    DETAIL = "ROOM_NOT_FOUND"
