from pydantic_settings import BaseSettings
from typing import List
from pathlib import Path
import json
import os

_DB_PATH = Path(__file__).resolve().parent.parent.parent / "referin.db"
_DEFAULT_DB = f"sqlite+aiosqlite:///{_DB_PATH}"


def _build_async_db_url() -> str:
    """Build the async database URL from environment.

    Render provides DATABASE_URL as postgresql://... which needs to be
    converted to postgresql+asyncpg://... for SQLAlchemy async.
    """
    url = os.environ.get("DATABASE_URL", _DEFAULT_DB)
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+asyncpg://", 1)
    elif url.startswith("postgresql://") and "+asyncpg" not in url:
        url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return url


class Settings(BaseSettings):
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    CORS_ORIGINS: str = '["http://localhost:5173","http://localhost:3000"]'

    @property
    def DATABASE_URL(self) -> str:
        return _build_async_db_url()

    @property
    def cors_origins_list(self) -> List[str]:
        if not self.CORS_ORIGINS:
            return ["http://localhost:5173", "http://localhost:3000"]
        return json.loads(self.CORS_ORIGINS)

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
