from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    APP_NAME: str = "My App"


class DatabaseSettings(BaseSettings):
    DATABASE_WORKER_ID: int = 268
    DATABASE_SALT_ROUNDS: int = 16
    SCHEME: str = "sqlite+aiosqlite:///"
    URL: str = SCHEME + str(
        Path(__file__).parent.parent / "database" / "database.sqlite3",
    )


class JWTSettings(BaseSettings):
    JWT_SECRET: str = "JWT_SECRET"
    JWT_ACCESS_TOKEN_EXPIRES_IN_MINUTES: int = 60
    JWT_REFRESH_TOKEN_EXPIRES_IN_DAYS: int = 30


class DevelopmentSettings(BaseSettings):
    DEVELOPMENT_HOST: str = "127.0.0.1"
    DEVELOPMENT_PORT: int = 26801
    DEVELOPMENT_TEST_PORT: int = 8001


class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    database: DatabaseSettings = DatabaseSettings()
    jwt: JWTSettings = JWTSettings()
    development: DevelopmentSettings = DevelopmentSettings()

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings: Settings = Settings()
