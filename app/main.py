from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.services.scraper import scrape_full_game_data
from app.services.matchups import build_matchup_objects


def create_app():
    app = FastAPI(
        title="MLB Matchups API",
        description="Backend powering the MLB analytics dashboard",
        version="1.0.0",
    )

    # ---------------------------------------------------------
    # CORS (required for Next.js frontend)
    # ---------------------------------------------------------
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],          # You can restrict this later
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ---------------------------------------------------------
    # Health check
    # ---------------------------------------------------------
    @app.get("/")
    def root():
        return {"status": "ok", "message": "MLB Matchups API running"}

    # ---------------------------------------------------------
    # Dashboard endpoint
    # ---------------------------------------------------------
    @app.get("/dashboard")
    def get_dashboard():
        games = scrape_full_game_data()
        matchups = build_matchup_objects(games)
        return {"games": matchups}

    return app


app = create_app()
