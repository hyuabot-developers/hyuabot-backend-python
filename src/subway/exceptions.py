from exceptions import Conflict, NotFound


class DuplicateStationName(Conflict):
    DETAIL = "DUPLICATE_STATION_NAME"


class StationNameNotFound(NotFound):
    DETAIL = "STATION_NAME_NOT_FOUND"


class DuplicateRouteID(Conflict):
    DETAIL = "DUPLICATE_ROUTE_ID"


class RouteNotFound(NotFound):
    DETAIL = "ROUTE_NOT_FOUND"


class DuplicateStationID(Conflict):
    DETAIL = "DUPLICATE_STATION_ID"


class StationNotFound(NotFound):
    DETAIL = "STATION_NOT_FOUND"


class DuplicateTimetable(Conflict):
    DETAIL = "DUPLICATE_TIMETABLE"


class TimetableNotFound(NotFound):
    DETAIL = "TIMETABLE_NOT_FOUND"
