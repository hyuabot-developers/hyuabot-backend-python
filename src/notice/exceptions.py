from exceptions import Conflict, NotFound


class DuplicateCategoryName(Conflict):
    DETAIL = "DUPLICATE_CATEGORY_NAME"


class CategoryNotFound(NotFound):
    DETAIL = "CATEGORY_NOT_FOUND"


class NoticeNotFound(NotFound):
    DETAIL = "NOTICE_NOT_FOUND"
