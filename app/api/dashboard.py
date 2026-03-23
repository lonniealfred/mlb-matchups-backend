# app/api/dashboard.py

from fastapi import APIRouter
from app.services.espn_scraper import build_dashboard
from app.services.demo_fallback import get_demo_dashboard

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard():
    """
    Returns today's MLB dashboard data.
    Attempts real scraping first.
    Falls back to demo dataset if scraping fails or returns empty data.
    """

    try:
        data = await build_dashboard()

        # Bulletproof fallback logic
        if (
            not data
            or "matchups" not in data
            or not isinstance(data["matchups"], list)
            or len(data["matchups"]) == 0
        ):
            print("⚠️ Using demo fallback — scraper returned no matchups.")
            return get_demo_dashboard()

        return data

    except Exception as e:
        print("❌ Scraper crashed — using demo fallback:", e)
        return get_demo_dashboard()
