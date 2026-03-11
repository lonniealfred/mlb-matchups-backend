# app/config.py

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # ---------------------------------------------------------
    # App settings
    # ---------------------------------------------------------
    app_env: str = Field(default="development")
    app_name: str = Field(default="mlb-matchups")
    app_debug: bool = Field(default=True)

    # ---------------------------------------------------------
    # Logging
    # ---------------------------------------------------------
    log_level: str = Field(default="INFO")
    file_logging_enabled: bool = Field(default=False)

    # ---------------------------------------------------------
    # ESPN scraping URLs
    # ---------------------------------------------------------
    espn_scoreboard_url: str = Field(
        default="https://site.web.api.espn.com/apis/v2/sports/baseball/mlb/scoreboard"
    )
    espn_player_stats_url: str = Field(
        default="https://sports.core.api.espn.com/v2/sports/baseball/leagues/mlb/athletes"
    )
    espn_venue_url: str = Field(
        default="https://sports.core.api.espn.com/v2/sports/baseball/leagues/mlb/venues"
    )

    # ---------------------------------------------------------
    # Scraper behavior
    # ---------------------------------------------------------
    enable_scraper_cache: bool = Field(default=False)

    # ---------------------------------------------------------
    # Future expansion (DB, Redis, etc.)
    # ---------------------------------------------------------
    database_url: str | None = None
    redis_url: str | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
