# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.dashboard import router as dashboard_router
from app.api.player_search import router as player_search_router
from app.api.game_details import router as game_details_router


def create_app() -> FastAPI:
    """
    Creates and configures the FastAPI application.
    This pattern avoids circular imports and keeps the app clean.
    """

    app = FastAPI(
        title="MLB Matchups API",
        version="1.0.0",
        description="Live MLB matchup, hitter, pitcher, and trends analytics backend."
    )

    # -----------------------------
    # CORS (allow your Next.js frontend)
    # -----------------------------
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # tighten later if needed
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # -----------------------------
    # Routers
    # -----------------------------
    app.include_router(dashboard_router)
    app.include_router(player_search_router)
    app.include_router(game_details_router)

    return app


# FastAPI entrypoint for Uvicorn / Render
app = create_app()
