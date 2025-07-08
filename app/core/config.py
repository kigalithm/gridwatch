from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    PROJECT_NAME: str = "GridWatch API"
    API_VERSION_STR: str = "/api/v1"
    DEBUG: bool = False
    ENV: str = "production"

    DATABASE_URL: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    CORS_ORIGINS: List[str] = ["*"]

    class Config:
        env_file = ".env"


settings = Settings()
