# app/api/dashboard.py

from fastapi import APIRouter
from app.services.espn_scraper import build_dashboard

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard():
    """
    Unified dashboard endpoint.
    Calls build_dashboard() which fetches:
      - scoreboard
      - boxscores
      - matchups
      - pitchers
      - hitters
      - analytics
    """
    data = await build_dashboard()

    # If ESPN is down or returns nothing, keep the API stable
    if not data:
        return {
            "matchups": [],
            "pitchers": [],
            "hitters": [],
            "status": "unavailable"
        }

    return data
