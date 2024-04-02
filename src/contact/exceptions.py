from exceptions import Conflict, NotFound


class DuplicateCategoryName(Conflict):
    DETAIL = "DUPLICATE_CATEGORY_NAME"


class CategoryNotFound(NotFound):
    DETAIL = "CATEGORY_NOT_FOUND"


class ContactNotFound(NotFound):
    DETAIL = "CONTACT_NOT_FOUND"
