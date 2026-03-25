from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.mode import router as mode_router
from app.api.scraper_status import router as scraper_status_router
from app.services.dashboard_live import build_live_dashboard


def create_app():
    app = FastAPI(
        title="MLB Matchups API",
        version="1.0.0",
    )

    # ---------------------------------------------------------
    # CORS (Frontend → Backend)
    # ---------------------------------------------------------
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],   # You can restrict this later
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ---------------------------------------------------------
    # ROUTERS
    # ---------------------------------------------------------
    app.include_router(mode_router)
    app.include_router(scraper_status_router)

    # ---------------------------------------------------------
    # /dashboard endpoint (async)
    # ---------------------------------------------------------
    @app.get("/dashboard")
    async def dashboard():
        return await build_live_dashboard()

    return app


app = create_app()
