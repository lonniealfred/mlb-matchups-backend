from fastapi import APIRouter
from app.scrapers.mlb_scoreboard import fetch_scoreboard
from app.services.matchups import extract_matchups

router = APIRouter()

@router.get("/matchups")
def get_matchups():
    try:
        # Scraper returns: { "events": [ ...game objects... ] }
        scoreboard = fetch_scoreboard()

        # Service returns the list of games
        games = extract_matchups(scoreboard)

        return {
            "status": "ok",
            "games": games,
            "message": ""
        }

    except Exception as e:
        return {
            "status": "error",
            "games": [],
            "message": f"Failed to load matchups: {e}"
        }
