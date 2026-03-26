from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Dashboard builder + legacy status
from app.services.dashboard_live import build_live_dashboard, get_scraper_status

# Scrapers / services that produce the required data
from app.scrapers.mlb_scoreboard import get_scoreboard
from app.services.hitters_leaderboard import build_hitter_leaderboard
from app.scrapers.mlb_trends import get_trends


app = FastAPI(title="MLB Matchups Backend")


# ---------------------------------------------------------
# CORS (required for your Next.js frontend)
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten later if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# /dashboard — main endpoint used by your frontend
# ---------------------------------------------------------
@app.get("/dashboard")
async def dashboard():
    # 1. Fetch live games
    games = await get_scoreboard()

    # 2. Build hitter rankings
    hitter_rankings = await build_hitter_leaderboard()

    # 3. Stadium HR factor trends
    stadium_factors = await get_trends()

    # 4. Build enriched dashboard payload
    return build_live_dashboard(games, hitter_rankings, stadium_factors)


# ---------------------------------------------------------
# /mode — legacy endpoint (frontend still calls this)
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
