# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.dashboard import router as dashboard_router
from app.api.mode import router as mode_router

app = FastAPI(
    title="MLB Matchups API",
    version="1.0.0",
)

# CORS (allow frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(dashboard_router)
app.include_router(mode_router)


@app.get("/")
def root():
    return {"status": "MLB Matchups API running"}
