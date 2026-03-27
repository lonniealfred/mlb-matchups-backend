from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.services.dashboard_live import build_live_dashboard, get_scraper_status
from app.scrapers.mlb_scoreboard import fetch_scoreboard
from app.services.hitters_leaderboard import build_hitters_leaderboard
from app.scrapers.mlb_trends import fetch_trends

# ⭐ ADD THIS
from app.api.routes import matchups, pitching

app = FastAPI(title="MLB Matchups Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ⭐ REGISTER YOUR ROUTES
app.include_router(matchups.router)
app.include_router(pitching.router)

@app.get("/dashboard")
async def dashboard():
    games = fetch_scoreboard()
    hitter_rankings = build_hitters_leaderboard(games)
    stadium_factors = fetch_trends()
    return build_live_dashboard(games, hitter_rankings, stadium_factors)

@app.get("/mode")
async def mode():
    return get_scraper_status()

@app.get("/")
async def root():
    return {"status": "ok", "message": "MLB Matchups Backend Running"}
