# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Correct import path based on your folder structure
from app.api.dashboard import router as dashboard_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="MLB Matchups API",
        version="1.0.0",
        description="Backend powering the MLB Matchups dashboard.",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # tighten later if you want
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register the dashboard router
    app.include_router(dashboard_router)

    return app


app = create_app()
