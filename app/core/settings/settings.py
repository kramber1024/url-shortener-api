from typing import Annotated, Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    NAME: Annotated[str, Field(min_length=1)] = "ushort"

    model_config = SettingsConfigDict(
        str_strip_whitespace=True,
        env_prefix="APP_",
    )


class DatabaseSettings(BaseSettings):
    URL: Annotated[str, Field(min_length=1)] = ""
    MACHINE_ID: Annotated[int, Field(gt=0, lt=1024)] = -1
    SALT_ROUNDS: Annotated[int, Field(ge=4)] = -1

    model_config = SettingsConfigDict(
        env_prefix="DATABASE_",
    )


class JWTSettings(BaseSettings):
    SECRET: Annotated[str, Field(min_length=1)] = ""
    ACCESS_TOKEN_EXPIRES_IN_MINUTES: Annotated[int, Field(ge=15)] = -1
    REFRESH_TOKEN_EXPIRES_IN_DAYS: Annotated[int, Field(ge=1)] = -1
    ALGORITHM: Literal["HS256"] = "HS256"

    model_config = SettingsConfigDict(
        env_prefix="JWT_",
    )


class DevelopmentSettings(BaseSettings):
    HOST: Annotated[str, Field(min_length=8)] = ""
    PORT: Annotated[int, Field(gt=0, lt=65536)] = -1
    TEST_PORT: Annotated[int, Field(gt=0, lt=65536)] = -1

    model_config = SettingsConfigDict(
        env_prefix="DEVELOPMENT_",
    )


class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    database: DatabaseSettings = DatabaseSettings()
    jwt: JWTSettings = JWTSettings()
    development: DevelopmentSettings = DevelopmentSettings()

    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings: Settings = Settings()
"""The application settings."""
