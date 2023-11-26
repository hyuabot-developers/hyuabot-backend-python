from exceptions import Unauthorized, PermissionDenied, BadRequest


class AuthRequired(Unauthorized):
    DETAIL = "AUTH_REQUIRED"


class AuthorizationFailed(PermissionDenied):
    DETAIL = "AUTHORIZATION_FAILED"


class InvalidCredentials(Unauthorized):
    DETAIL = "INVALID_CREDENTIALS"


class InvalidRefreshToken(Unauthorized):
    DETAIL = "INVALID_REFRESH_TOKEN"


class InvalidAccessToken(Unauthorized):
    DETAIL = "INVALID_ACCESS_TOKEN"


class EmailAlreadyExists(BadRequest):
    DETAIL = "EMAIL_ALREADY_EXISTS"
