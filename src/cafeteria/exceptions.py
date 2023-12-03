from exceptions import Conflict, NotFound, BadRequest


class DuplicateCafeteriaID(Conflict):
    DETAIL = "DUPLICATE_CAFETERIA_ID"


class CafeteriaNotFound(NotFound):
    DETAIL = "CAFETERIA_NOT_FOUND"


class InvalidCampusID(BadRequest):
    DETAIL = "INVALID_CAMPUS_ID"


class DuplicateMenuID(Conflict):
    DETAIL = "DUPLICATE_MENU_ID"


class MenuNotFound(NotFound):
    DETAIL = "MENU_NOT_FOUND"


class InvalidCafeteriaID(BadRequest):
    DETAIL = "INVALID_CAFETERIA_ID"
