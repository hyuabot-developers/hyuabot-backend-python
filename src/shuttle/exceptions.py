from exceptions import Conflict, NotFound


class DuplicateHolidayDate(Conflict):
    DETAIL = "DUPLICATE_HOLIDAY_DATE"


class HolidayNotFound(NotFound):
    DETAIL = "HOLIDAY_NOT_FOUND"


class DuplicatePeriod(Conflict):
    DETAIL = "DUPLICATE_PERIOD"


class PeriodNotFound(NotFound):
    DETAIL = "PERIOD_NOT_FOUND"


class DuplicateRouteName(Conflict):
    DETAIL = "DUPLICATE_ROUTE_NAME"


class RouteNotFound(NotFound):
    DETAIL = "ROUTE_NOT_FOUND"


class DuplicateStopName(Conflict):
    DETAIL = "DUPLICATE_STOP_NAME"


class StopNotFound(NotFound):
    DETAIL = "STOP_NOT_FOUND"


class DuplicateRouteStop(Conflict):
    DETAIL = "DUPLICATE_ROUTE_STOP"


class RouteStopNotFound(NotFound):
    DETAIL = "ROUTE_STOP_NOT_FOUND"


class DuplicateTimetableSequence(Conflict):
    DETAIL = "DUPLICATE_TIMETABLE_SEQUENCE"


class TimetableNotFound(NotFound):
    DETAIL = "TIMETABLE_NOT_FOUND"
