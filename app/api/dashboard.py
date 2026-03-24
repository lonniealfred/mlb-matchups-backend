# app/api/dashboard.py

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.services.dashboard_live import build_live_dashboard
from app.services.demo_fallback import get_demo_dashboard

router = APIRouter()


@router.get("/dashboard")
def get_dashboard():
    """
    Live-first MLB dashboard endpoint.
    - Attempts to build live data from scrapers
    - If scrapers fail OR return no matchups → fallback to demo data
    - Ensures the frontend always receives a complete, valid payload
    """

    try:
        live = build_live_dashboard()

        # If live data exists and has matchups, return it
        if (
            isinstance(live, dict)
            and live.get("matchups")
            and len(live["matchups"]) > 0
        ):
            return JSONResponse(content=live)

    except Exception as e:
        # Log scraper errors to Render logs
        print("LIVE SCRAPER ERROR:", e)

    # Fallback: always return demo data so UI never breaks
    return JSONResponse(content=get_demo_dashboard())
