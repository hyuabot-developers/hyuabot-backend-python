from exceptions import Conflict, NotFound


class DuplicateRouteName(Conflict):
    DETAIL = "DUPLICATE_ROUTE_NAME"


class RouteNotFound(NotFound):
    DETAIL = "ROUTE_NOT_FOUND"


class DuplicateStopName(Conflict):
    DETAIL = "DUPLICATE_STOP_NAME"


class StopNotFound(NotFound):
    DETAIL = "STOP_NOT_FOUND"


class DuplicateTimetableSequence(Conflict):
    DETAIL = "DUPLICATE_TIMETABLE_SEQUENCE"


class TimetableNotFound(NotFound):
    DETAIL = "TIMETABLE_NOT_FOUND"
