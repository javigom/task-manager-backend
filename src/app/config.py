from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Configured for Docker-based development and deployment.
    For production, override sensitive values via environment variables.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Database configuration (defaults configured for Docker)
    DB_USER: str = "taskuser"
    DB_PASSWORD: str = "taskpass"
    DB_HOST: str = "db"
    DB_PORT: int = 5432
    DB_NAME: str = "taskdb"

    # JWT configuration
    SECRET_KEY: str = "dev-secret-key-change-in-production-use-openssl-rand-hex-32"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days

    # CORS configuration
    CORS_ORIGINS: str = "*"  # Comma-separated list of origins

    # Environment
    ENVIRONMENT: str = "development"
    # Whether to run Base.metadata.create_all() on startup. Prefer False and use Alembic for schema management.
    INIT_DB: bool = False

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        """Construct database URL from components."""
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins from comma-separated string."""
        if self.CORS_ORIGINS == "*":
            return ["*"]
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


settings = Settings()
