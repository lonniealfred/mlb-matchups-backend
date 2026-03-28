from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create the FastAPI app FIRST — before any decorators
app = FastAPI(title="MLB Matchups Backend")

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Now import everything else
from app.services.dashboard_live import build_live_dashboard, get_scraper_status
from app.scrapers.mlb_scoreboard import fetch_scoreboard
from app.services.hitters_leaderboard import build_hitters_leaderboard
from app.scrapers.mlb_trends import fetch_trends
from app.api.routes import matchups, pitching

# Register routers
app.include_router(matchups.router)
app.include_router(pitching.router)


# -------------------------
#       DASHBOARD
# -------------------------
@app.get("/dashboard")
async def dashboard():
    # Fetch scoreboard (returns {"events": [...]})
    scoreboard = fetch_scoreboard()
    games = scoreboard.get("events", [])

    # Build hitter rankings using the list of game dicts
    hitter_rankings = build_hitters_leaderboard(games)

    # Stadium factors / trends
    stadium_factors = fetch_trends()

    # Build final dashboard payload
    return build_live_dashboard(games, hitter_rankings, stadium_factors)


# -------------------------
#       MODE
# -------------------------
@app.get("/mode")
async def mode():
    return get_scraper_status()


# -------------------------
#       ROOT
# -------------------------
@app.get("/")
async def root():
    return {"status": "ok", "message": "MLB Matchups Backend Running"}
