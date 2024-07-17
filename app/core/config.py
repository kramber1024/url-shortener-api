from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIRERCTORY = Path(__file__).parent


class DatabaseSettings(BaseSettings):
    WORKER_ID: int = 268
    SCHEME: str = "sqlite+aiosqlite:///"
    URL: str = SCHEME + str(BASE_DIRERCTORY / "database" / "database.sqlite3")
    SALT_ROUNDS: int = 16


class JWTSettings(BaseSettings):
    ALGORITHM: Literal["HS256"] = "HS256"
    SECRET: str = "SET_ME_IN_ENV"
    ACCESS_TOKEN_EXPIRES_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRES_DAYS: int = 30


class DevelopmentSettings(BaseSettings):
    HOST: str = "127.0.0.1"
    PORT: int = 26801


class AppSettings(BaseSettings):
    NAME: str = ""


class Settings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()
    jwt: JWTSettings = JWTSettings()
    dev: DevelopmentSettings = DevelopmentSettings()
    app: AppSettings = AppSettings()

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings: Settings = Settings()
