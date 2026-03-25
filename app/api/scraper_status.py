from fastapi import APIRouter
from app.services.dashboard_live import get_scraper_status

router = APIRouter()

@router.get("/scraper/status")
def scraper_status():
    return get_scraper_status()
