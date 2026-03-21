from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Environment
    ENV: str = Field(default="production")
    DEBUG: bool = Field(default=False)

    # Scraper settings
    SCRAPER_MODE: str = Field(default="live")  # "live" or "demo"
    CACHE_ENABLED: bool = Field(default=True)

    # Optional API keys
    RAPIDAPI_KEY: str | None = None

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
