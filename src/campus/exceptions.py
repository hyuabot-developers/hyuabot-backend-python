from exceptions import Conflict, NotFound


class DuplicateCampusID(Conflict):
    DETAIL = "DUPLICATE_CAMPUS_ID"


class CampusNotFound(NotFound):
    DETAIL = "CAMPUS_NOT_FOUND"
