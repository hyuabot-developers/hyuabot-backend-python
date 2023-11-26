from typing import Any

from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from constants import Environment


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
    DATABASE_URL: PostgresDsn
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    REDIS_URL: RedisDsn

    SITE_DOMAIN: str = "hyuabot.app"
    ENVIRONMENT: Environment = Environment.PRODUCTION

    CORS_ORIGINS: list[str]
    CORS_ORIGIN_REGEX: str | None = None
    CORS_HEADERS: list[str]

    JWT_ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str
    JWT_EXPIRATION: int = 60 * 60 * 24 * 7  # 7 days

    APP_VERSION: str = "1"


settings = Config()

app_configs: dict[str, Any] = {"title": "HYUabot API", "version": settings.APP_VERSION}
if settings.ENVIRONMENT.is_deployed:
    app_configs["root_path"] = "/api/v1"

if not settings.ENVIRONMENT.is_debug:
    app_configs["docs_url"] = None
    app_configs["redoc_url"] = None
    app_configs["openapi_url"] = None
