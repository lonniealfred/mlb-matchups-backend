# app/api/dashboard.py

from fastapi import APIRouter

from app.services.espn_scraper import build_dashboard
from app.services.team_data import get_stadium_factors   # ← NEW IMPORT

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard():
    """
    Unified dashboard endpoint.
    Returns:
      - matchups
      - pitchers
      - hitters
      - stadium_factors  ← added for TrendsView
    """
    data = await build_dashboard()

    # ESPN down? Keep API stable
    if not data:
        return {
            "matchups": [],
            "pitchers": [],
            "hitters": [],
            "stadium_factors": [],
            "status": "unavailable"
        }

    # Add stadium factors to the response
    stadium_factors = get_stadium_factors()

    return {
        **data,
        "stadium_factors": stadium_factors
    }
