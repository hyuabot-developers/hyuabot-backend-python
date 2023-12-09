from exceptions import Conflict, NotFound


class DuplicateRouteID(Conflict):
    DETAIL = "DUPLICATE_ROUTE_ID"


class RouteNotFound(NotFound):
    DETAIL = "ROUTE_NOT_FOUND"


class DuplicateStopID(Conflict):
    DETAIL = "DUPLICATE_STOP_ID"


class StopNotFound(NotFound):
    DETAIL = "STOP_NOT_FOUND"


class DuplicateRouteStop(Conflict):
    DETAIL = "DUPLICATE_ROUTE_STOP"


class RouteStopNotFound(NotFound):
    DETAIL = "ROUTE_STOP_NOT_FOUND"


class DuplicateTimetable(Conflict):
    DETAIL = "DUPLICATE_TIMETABLE"


class StartStopNotFound(NotFound):
    DETAIL = "START_STOP_NOT_FOUND"


class TimetableNotFound(NotFound):
    DETAIL = "TIMETABLE_NOT_FOUND"


class RealtimeNotFound(NotFound):
    DETAIL = "REALTIME_NOT_FOUND"
