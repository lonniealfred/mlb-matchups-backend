# app/routers/dashboard.py

from fastapi import APIRouter
from app.services.espn_scraper import build_dashboard
from app.services.demo_fallback import get_demo_dashboard

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard():
    """
    Returns the full MLB dashboard:
    - matchups
    - pitchers
    - hitters
    """
    try:
        data = await build_dashboard()
        return data
    except Exception:
        return get_demo_dashboard()
