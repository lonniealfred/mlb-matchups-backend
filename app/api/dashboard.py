# app/api/dashboard.py

from fastapi import APIRouter

# Import from the REAL location of your logic
from app.services.matchups import get_matchups
from app.services.pitchers import get_pitcher_scores
from app.services.hitters import get_hitter_scores
from app.services.weather import get_weather_factors
from app.services.team_data import get_stadium_factors

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard():
    """
    Aggregate all dashboard data into a single response.
    This is what your Next.js frontend calls via apiGet("/dashboard").
    """
    matchups = await get_matchups()
    pitchers = await get_pitcher_scores()
    hitters = await get_hitter_scores()
    weather = await get_weather_factors()
    stadiums = await get_stadium_factors()

    return {
        "matchups": matchups,
        "pitchers": pitchers,
        "hitters": hitters,
        "weather": weather,
        "stadiums": stadiums,
    }
