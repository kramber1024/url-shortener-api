from pathlib import Path
from typing import Literal, TypeAlias

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIRERCTORY = Path(__file__).parent

JWTAlgorithm: TypeAlias = Literal["HS256"]


class DatabaseSettings(BaseSettings):
    WORKER_ID: int = 268
    SCHEME: str = "sqlite+aiosqlite:///"
    URL: str = SCHEME + str(BASE_DIRERCTORY / "database" / "database.sqlite3")
    SALT_ROUNDS: int = 16


class JWTSettings(BaseSettings):
    ALGORITHM: JWTAlgorithm = "HS256"
    SECRET: str = "CHANGE_ME_IN_ENV"
    ACCESS_TOKEN_EXPIRES_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRES_DAYS: int = 30


class DevelopmentSettings(BaseSettings):
    HOST: str = "127.0.0.1"
    PORT: int = 26801
    TEST_PORT: int = 8001


class AppSettings(BaseSettings):
    NAME: str = ""


class DataSettings(BaseSettings):
    FIRST_NAME_MIN_LENGTH: int = 3
    FIRST_NAME_MAX_LENGTH: int = 16
    LAST_NAME_MIN_LENGTH: int = 3
    LAST_NAME_MAX_LENGTH: int = 16
    EMAIL_MIN_LENGTH: int = len("a@b.c")
    EMAIL_MAX_LENGTH: int = 64
    PHONE_MIN_LENGTH: int = 7
    PHONE_MAX_LENGTH: int = 16
    PASSWORD_MIN_LENGTH: int = 8
    PASSWORD_MAX_LENGTH: int = 256
    SHORT_URL_MIN_LENGTH: int = len("a")
    SHORT_URL_MAX_LENGTH: int = 256
    SHORT_URL_MAX_TAGS_COUNT: int = 32
    URL_MIN_LENGTH: int = len("http://a.b")
    URL_MAX_LENGTH: int = 2048
    TAG_MIN_LENGTH: int = len("a")
    TAG_MAX_LENGTH: int = 32
    UNKNOWN_COUNTRY_CODE: str = "ZZ"
    UNKNOWN_IP_ADDRESS: str = "255.255.255.255"


class Settings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()
    data: DataSettings = DataSettings()
    jwt: JWTSettings = JWTSettings()
    dev: DevelopmentSettings = DevelopmentSettings()
    app: AppSettings = AppSettings()

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings: Settings = Settings()
