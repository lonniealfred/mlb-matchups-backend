from fastapi import APIRouter

# Import your existing data functions
from .matchups import get_matchups
from .pitchers import get_pitcher_scores
from .hitters import get_hitter_scores
from .weather import get_weather_factors
from .stadiums import get_stadium_factors

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard():
    """
    Aggregate all dashboard data into a single response.
    This endpoint is what your Next.js frontend calls via apiGet("/dashboard").
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
