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

        # If scraper returns nothing or partial data, fallback to demo
        if (
            not data
            or not data.get("matchups")
            or len(data.get("matchups", [])) == 0
        ):
            print("⚠️ Scraper returned empty data — using demo fallback.")
            return get_demo_dashboard()

        # If scraper succeeded, return real data
        return data

    except Exception as e:
        print("❌ Scraper crashed — using demo fallback:", e)
        return get_demo_dashboard()
