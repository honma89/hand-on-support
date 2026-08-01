from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Centralized application configuration.

    All environment-dependent values live here. Nothing else in the
    codebase should call os.getenv() directly — this is the single
    source of truth, validated at process startup (fail fast).
    """

    # --- App ---
    APP_NAME: str = "Hand On Support API"
    APP_ENV: str = "development"  # development | staging | production
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    # --- Database ---
    DATABASE_URL: str  # e.g. postgresql+asyncpg://user:pass@db:5432/handonsupport

    # --- Auth / JWT (wired up fully in Module 1, declared now so the
    #     .env contract is stable from the start) ---
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # --- CORS ---
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost"]

    # --- File uploads (local disk for now; see FileStorageRepository for
    #     the swap point when this needs to move to cloud storage) ---
    UPLOAD_ROOT: str = "uploads"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Cached settings accessor. FastAPI dependencies should import and call
    this rather than instantiating Settings() directly, so the env file
    is parsed exactly once per process.
    """
    return Settings()
