import bcrypt


def hash_password(password: str) -> bytes:
    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt(),
    )
    return hashed_password


def verify_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password,
    )
