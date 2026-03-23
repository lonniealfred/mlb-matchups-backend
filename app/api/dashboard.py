# app/api/dashboard.py

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.services.demo_fallback import get_demo_dashboard
from app.services.dashboard_live import build_live_dashboard

router = APIRouter()


@router.get("/dashboard")
def get_dashboard():
    """
    Returns the MLB dashboard data.
    - First tries live scraper (dashboard_live)
    - Falls back to demo data if scraping fails or returns empty
    """

    try:
        live = build_live_dashboard()

        # If scraper returns valid matchups, use it
        if live and isinstance(live, dict) and live.get("matchups"):
            return JSONResponse(content=live)

        # Otherwise fallback
        return JSONResponse(content=get_demo_dashboard())

    except Exception as e:
        # Log error in Render logs
        print("LIVE SCRAPER ERROR:", e)

        # Always return fallback so frontend never breaks
        return JSONResponse(content=get_demo_dashboard())
