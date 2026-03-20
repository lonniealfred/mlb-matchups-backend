# app/routers/dashboard.py

from fastapi import APIRouter, HTTPException
from app.services.espn_scraper import build_dashboard

router = APIRouter()


@router.get("/dashboard")
async def get_dashboard():
    """
    Full dashboard payload:
      - matchups
      - hitters
      - pitchers
    """
    data = await build_dashboard()
    if not data:
        raise HTTPException(status_code=500, detail="Failed to build dashboard")
    return data


@router.get("/hitters")
async def get_hitters():
    """
    Top hitters only.
    """
    data = await build_dashboard()
    hitters = data.get("hitters", [])
    return {"hitters": hitters}


@router.get("/matchups")
async def get_matchups():
    """
    Matchups only.
    """
    data = await build_dashboard()
    matchups = data.get("matchups", [])
    return {"matchups": matchups}


@router.get("/pitchers")
async def get_pitchers():
    """
    Pitchers only.
    """
    data = await build_dashboard()
    pitchers = data.get("pitchers", [])
    return {"pitchers": pitchers}
