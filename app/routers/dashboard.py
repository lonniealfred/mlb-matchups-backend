# app/routers/dashboard.py

from fastapi import APIRouter
from datetime import datetime

from app.schemas import DashboardResponse, HitStreak
from app.services.matchups import build_matchup_objects

router = APIRouter()


@router.get("/dashboard", response_model=DashboardResponse)
def get_dashboard():
    """
    Returns the full MLB dashboard payload:
    - Fully scored games
    - Global hit streak leaderboard (optional placeholder)
    """

    games = build_matchup_objects()

    # Placeholder hit streaks until you implement a real global streak scraper
    hit_streaks = [
        HitStreak(
            player="Example Player",
            team="NYY",
            streak=7,
            today_opponent="BOS",
            today_pitcher="Chris Sale"
        )
    ]

    return DashboardResponse(
        date=datetime.now().strftime("%Y-%m-%d"),
        games=games,
        hit_streaks=hit_streaks
    )
