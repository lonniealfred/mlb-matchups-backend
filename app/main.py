# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import your router directly
from app.routers.dashboard import router as dashboard_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="MLB Matchups API",
        version="1.0.0",
        description="Backend powering the MLB Matchups dashboard."
    )

    # CORS for your Next.js frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # replace with your frontend domain later
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register the router
    app.include_router(dashboard_router)

    return app


app = create_app()
