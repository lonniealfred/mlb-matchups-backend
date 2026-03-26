from fastapi import APIRouter
from app.services.pitching import get_pitching_rankings, get_demo_pitching
from app.services.mlb_pitchers import fetch_pitchers_from_espn  # if you have this scraper

router = APIRouter()


@router.get("/pitching")
def get_pitching():
    """
    Returns ranked pitchers using the Pitcher Ranking System (Rules 1–4).
    Automatically falls back to demo mode if ESPN returns no data.
    """

    try:
        # Attempt to fetch live pitcher data
        raw_pitchers = fetch_pitchers_from_espn()

        # If ESPN returns nothing, fallback to demo
        if not raw_pitchers:
            pitchers = get_demo_pitching()
            return {
                "status": "demo",
                "message": "Using demo pitching data (no live data available)",
                "pitchers": pitchers,
            }

        # Live mode
        pitchers = get_pitching_rankings(raw_pitchers)
        return {
            "status": "live",
            "message": "Live pitching data retrieved successfully",
            "pitchers": pitchers,
        }

    except Exception as e:
        # Hard fallback — never break the UI
        pitchers = get_demo_pitching()
        return {
            "status": "error",
            "message": f"Pitching endpoint failed, using demo data: {str(e)}",
            "pitchers": pitchers,
        }
