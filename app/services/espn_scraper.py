# app/services/espn_scraper.py

import httpx
from app.config import settings
from app.services.demo_fallback import get_demo_dashboard
from app.services.matchups import extract_matchups
from app.services.scoring import score_hitters

ESPN_SCOREBOARD_URL = (
    "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard"
)

async def fetch_json(url: str):
    """Safe JSON fetch with graceful fallback."""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(url)
            r.raise_for_status()
            return r.json()
    except Exception:
        return None


async def build_dashboard():
    """
    Main entrypoint for the backend.
    Returns a dict containing:
      - matchups
      - hitters
      - pitchers
    Always returns valid data (fallback if needed).
    """

    # DEMO MODE (forced)
    if settings.SCRAPER_MODE.lower() == "demo":
        return get_demo_dashboard()

    # LIVE MODE
    data = await fetch_json(ESPN_SCOREBOARD_URL)

    # If ESPN fails → fallback
    if not data:
        return get_demo_dashboard()

    # Extract matchups
    matchups = extract_matchups(data)

    # Extract hitters from matchups
    hitters = []
    for m in matchups:
        hitters.extend(m.get("top_hitters", []))

    # Score hitters
    scored_hitters = score_hitters(hitters)

    return {
        "matchups": matchups,
        "hitters": scored_hitters,
        "pitchers": [m["home_pitcher"] for m in matchups]
                    + [m["away_pitcher"] for m in matchups],
    }
