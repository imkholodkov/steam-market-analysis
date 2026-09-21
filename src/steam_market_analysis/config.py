from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="RG_", env_file=".env", extra="ignore")

    github_token: str | None = None
    data_dir: Path = Path("data")
    log_level: str = "INFO"
    request_timeout: float = Field(default=10.0, gt=0)
    max_concurrency: int = Field(default=4, ge=1)

    def ensure_data_dir(self) -> Path:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        return self.data_dir


def get_settings() -> Settings:
    return Settings()
