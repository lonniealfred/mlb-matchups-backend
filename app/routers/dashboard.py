from fastapi import APIRouter
from app.services.espn_scraper import get_mlb_games_with_hitters

router = APIRouter()

@router.get("/dashboard")
def dashboard():
    games = get_mlb_games_with_hitters()
    return {"games": games}
