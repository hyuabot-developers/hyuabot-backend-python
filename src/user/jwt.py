import datetime

import pytz
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from model.user import User
from user.config import auth_config
from user.exceptions import InvalidAccessToken

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/users/token", auto_error=False)


def create_access_token(
    *,
    user: User,
    expires_delta: datetime.timedelta = datetime.timedelta(minutes=auth_config.JWT_EXP),
) -> str:
    payload = {
        "sub": user._id,
        "exp": datetime.datetime.now(pytz.timezone("Asia/Seoul")) + expires_delta,
    }

    return jwt.encode(
        payload,
        auth_config.JWT_SECRET,
        algorithm=auth_config.JWT_ALG,
    )


def parse_jwt_user_data_optional(
    token: str = Depends(oauth2_scheme),
) -> str | None:
    if token is None:
        return None

    try:
        payload = jwt.decode(
            token,
            auth_config.JWT_SECRET,
            algorithms=[auth_config.JWT_ALG],
        )
    except jwt.JWTError:
        raise InvalidAccessToken()

    return payload["sub"]


def parse_jwt_user_data(
    user_id: str = Depends(parse_jwt_user_data_optional),
) -> str:
    if user_id is None:
        raise InvalidAccessToken()

    return user_id
