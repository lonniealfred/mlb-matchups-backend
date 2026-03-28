from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.scrapers.mlb_scoreboard import fetch_scoreboard
from app.services.matchups import extract_matchups
from app.services.hitters_leaderboard import build_hitter_leaderboard
from app.scrapers.mlb_trends import fetch_stadium_trends
from app.services.dashboard_live import build_live_dashboard

router = APIRouter()

@router.get("/dashboard")
def get_dashboard():
    try:
        # 1. Fetch games
        scoreboard = fetch_scoreboard()
        games = extract_matchups(scoreboard)

        # 2. Hitter rankings (NO arguments)
        hitter_rankings = build_hitter_leaderboard()

        # 3. Stadium HR trends
        stadium_factors = fetch_stadium_trends()

        # 4. Build full dashboard payload
        data = build_live_dashboard(games, hitter_rankings, stadium_factors)

        return JSONResponse(content=data)

    except Exception as e:
        return JSONResponse(
            content={
                "status": "error",
                "games": [],
                "hitters": [],
                "trends": [],
                "message": f"Dashboard failed: {e}",
            },
            status_code=500
        )
