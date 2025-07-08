from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    PROJECT_NAME: str = "GridWatch API"
    API_VERSION_STR: str = "/api/v1"
    DEBUG: bool = False
    ENV: str = "production"
    API_BASE_URL: str

    DATABASE_URL: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    CORS_ORIGINS: List[str] = ["*"]

    BEARER_TOKEN: str
    CONSUMER_KEY: str
    CONSUMER_SECRET: str
    ACCESS_TOKEN: str
    ACCESS_TOKEN_SECRET: str

    TWITTER_API_LIMIT: int
    COOLDOWN_SECONDS: int

    class Config:
        env_file = ".env"


settings = Settings()
