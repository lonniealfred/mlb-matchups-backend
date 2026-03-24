# app/api/player_search.py

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from app.data.player_data import load_player_ids

router = APIRouter()


@router.get("/player/search")
def search_players(q: str = Query(..., min_length=1)):
    """
    Autocomplete search for player names.
    Example:
        /player/search?q=jud
    """

    q_lower = q.lower()
    players = load_player_ids()

    matches = [
        {"name": name, "player_id": pid}
        for name, pid in players.items()
        if q_lower in name.lower()
    ]

    return JSONResponse(content=matches[:20])
