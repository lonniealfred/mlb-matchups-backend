from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Dashboard builder + legacy status
from app.services.dashboard_live import build_live_dashboard, get_scraper_status

# Correct imports based on your actual function names
from app.scrapers.mlb_scoreboard import fetch_scoreboard
from app.services.hitters_leaderboard import build_hitters_leaderboard
from app.scrapers.mlb_trends import get_trends


app = FastAPI(title="MLB Matchups Backend")


# ---------------------------------------------------------
# CORS (for your Next.js frontend)
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# /dashboard — main endpoint
# ---------------------------------------------------------
@app.get("/dashboard")
async def dashboard():
    # 1. Live games
    games = await fetch_scoreboard()

    # 2. Hitter rankings
    hitter_rankings = await build_hitters_leaderboard()

    # 3. Stadium HR trends
    stadium_factors = await get_trends()

    # 4. Build enriched dashboard payload
    return build_live_dashboard(games, hitter_rankings, stadium_factors)


# ---------------------------------------------------------
# /mode — legacy endpoint
# ---------------------------------------------------------
@app.get("/mode")
async def mode():
    return get_scraper_status()


# ---------------------------------------------------------
# Root endpoint
# ---------------------------------------------------------
@app.get("/")
async def root():
    return {"status": "ok", "message": "MLB Matchups Backend Running"}
