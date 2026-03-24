from fastapi import APIRouter
from app.services.dashboard_live import get_dashboard_mode

router = APIRouter()

@router.get("/mode")
def mode_status():
    """
    Returns whether the dashboard is in live mode or demo mode.
    """
    return {"mode": get_dashboard_mode()}
