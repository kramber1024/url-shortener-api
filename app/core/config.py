from pathlib import Path
from typing import Annotated, Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIRERCTORY = Path(__file__).parent


class SnowflakeSettings(BaseSettings):
    WORKER_ID: int = 999  # Value in range [1, 1023]


class DatabaseSettings(BaseSettings):
    gen: SnowflakeSettings = SnowflakeSettings()
    SCHEME: str = "sqlite+aiosqlite:///"
    URL: str = SCHEME + str(BASE_DIRERCTORY / "database" / "database.sqlite3")
    SALT_ROUNDS: int = 16


class JWTSettings(BaseSettings):
    ALGORITHM: Literal["HS256"] = "HS256"
    SECRET: Annotated[str, Field(json_schema_extra={"env": "JWT_SECRET"})] = ""
    ACCESS_TOKEN_EXPIRES_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRES_DAYS: int = 30


class StateSettings(BaseSettings):
    PRODUCTION: Annotated[bool, Field(json_schema_extra={"env": "PRODUCTION"})] = False
    DEBUG: Annotated[bool, Field(json_schema_extra={"env": "DEBUG"})] = False


class AppSettings(BaseSettings):
    NAME: str = "ushort"
    state: StateSettings = StateSettings()


class EmailSettings(BaseSettings):
    VERIFICATION_EXPIRES_HOURS: int = 24


class Settings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()
    jwt: JWTSettings = JWTSettings()
    email: EmailSettings = EmailSettings()
    app: AppSettings = AppSettings()

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings: Settings = Settings()
