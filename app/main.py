from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import dashboard builder + scraper modules
from app.services.dashboard_live import build_live_dashboard, get_scraper_status
from app.services.schedule_scraper import get_games
from app.services.hitter_service import get_hitter_rankings
from app.services.stadium_factors import get_stadium_factors


app = FastAPI(title="MLB Matchups Backend")

# ---------------------------------------------------------
# CORS (required for Next.js frontend)
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # You can restrict this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# /dashboard — main endpoint used by your frontend
# ---------------------------------------------------------
@app.get("/dashboard")
async def dashboard():
    # Fetch all required data
    games = await get_games()
    hitter_rankings = await get_hitter_rankings()
    stadium_factors = await get_stadium_factors()

    # Build enriched dashboard payload
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
