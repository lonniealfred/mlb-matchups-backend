from fastapi import APIRouter
from app.services.pitching import fetch_pitchers_from_espn
from app.services.pitching_leaderboard import build_pitching_leaderboard

router = APIRouter()

@router.get("/pitching")
def get_pitching():
    try:
        # Fetch raw pitcher data (ESPN or fallback)
        pitchers = fetch_pitchers_from_espn()

        # Build leaderboard with scoring + sorting
        leaderboard = build_pitching_leaderboard(pitchers)

        return {
            "status": "ok",
            "pitchers": leaderboard,
            "message": ""
        }

    except Exception as e:
        return {
            "status": "error",
            "pitchers": [],
            "message": f"Failed to load pitching data: {e}"
        }
