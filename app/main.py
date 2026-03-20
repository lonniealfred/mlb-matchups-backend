# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import dashboard

app = FastAPI(
    title="MLB Matchups Backend",
    version="1.0.0",
)

# CORS (allow your frontend + local dev)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    # Add your Vercel URL here, e.g.:
    # "https://mlb-matchups-frontend.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["system"])
async def health_check():
    return {
        "status": "ok",
        "env": settings.ENV,
        "scraper_mode": settings.SCRAPER_MODE,
    }


# Routers
app.include_router(dashboard.router, prefix="/api", tags=["dashboard"])
