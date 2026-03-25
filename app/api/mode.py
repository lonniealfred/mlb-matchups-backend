from fastapi import APIRouter
from app.services.dashboard_live import get_scraper_status

router = APIRouter()

@router.get("/mode")
def mode():
    status = get_scraper_status()
    return {"mode": status["mode"]}
