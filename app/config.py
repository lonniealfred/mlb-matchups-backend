# app/config.py

from pydantic import BaseSettings

class Settings(BaseSettings):
    ENV: str = "development"
    SCRAPER_MODE: str = "live"  # "live" or "demo"
    CACHE_ENABLED: bool = True
    CACHE_TTL: int = 3600  # seconds
    LOG_LEVEL: str = "info"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
