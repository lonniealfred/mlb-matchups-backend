# app/routers/dashboard.py

from fastapi import APIRouter
from app.services.espn_scraper import build_dashboard
from app.services.demo_fallback import get_demo_dashboard

router = APIRouter()


@router.get("/dashboard")
async def get_dashboard():
    """
    Main dashboard endpoint.
    Attempts to fetch live ESPN data.
    Falls back to demo data if scraping fails.
    Always returns a complete, frontend-safe object.
    """
    try:
        data = await build_dashboard()
        return data
    except Exception:
        # Guaranteed fallback so the frontend never breaks
        return get_demo_dashboard()
