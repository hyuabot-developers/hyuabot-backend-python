from typing import Any

from config import settings
from user.config import auth_config


def get_refresh_token_settings(
    refresh_token: str,
    expired: bool = False,
) -> dict[str, Any]:
    base_cookie_settings = {
        "key": auth_config.REFRESH_TOKEN_KEY,
        "httponly": True,
        "samesite": "none",
        "secure": auth_config.SECURE_COOKIES,
        "domain": settings.SITE_DOMAIN,
    }

    if expired:
        return base_cookie_settings
    return {
        **base_cookie_settings,
        "value": refresh_token,
        "max_age": auth_config.REFRESH_TOKEN_EXP,
    }
