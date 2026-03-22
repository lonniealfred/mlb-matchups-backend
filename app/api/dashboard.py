from fastapi import APIRouter
from .matchups import get_matchups
from .pitchers import get_pitches_scores
from .hitters import get_hitter_scores
from .weather import get_weather_factors
from .stadiums import get_stadium_factors

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard():
    return {
        "matchups": await get_matchups(),
        "pitchers": await get_pitcher_scores(),
        "hitters": await get_hitter_scores(),
        "weather": await get_weather_factors(),
        "stadiums": await get_stadium_factors(),
    }
