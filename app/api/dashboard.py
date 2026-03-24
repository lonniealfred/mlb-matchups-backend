# app/api/dashboard.py

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.services.dashboard_live import build_live_dashboard

router = APIRouter()


@router.get("/dashboard")
def get_dashboard():
    """
    Returns the full live MLB dashboard:
    - Matchups
    - Pitchers
    - Hitters leaderboard
    - Top hitters
    - Trends
    """
    data = build_live_dashboard()
    return JSONResponse(content=data)
