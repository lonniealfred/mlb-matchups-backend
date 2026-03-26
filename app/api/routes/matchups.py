from fastapi import APIRouter
from app.services.matchups import build_matchups

router = APIRouter()

@router.get("/matchups")
def get_matchups():
    try:
        games = build_matchups()
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
