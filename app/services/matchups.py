# app/services/matchups.py

from typing import Dict, List, Any

def extract_matchups(scoreboard: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    The scraper (mlb_scoreboard.py) returns:
        { "events": [ { ...game... }, ... ] }

    Each game object is already fully processed:
        - home_team, away_team
        - logos
        - colors
        - pitchers (TBD for now)
        - featured hitters (TBD for now)
        - game_time, game_id

    So this function simply validates and returns the list.
    """

    # Ensure scoreboard is a dict
    if not isinstance(scoreboard, dict):
        return []

    events = scoreboard.get("events", [])

    # Ensure events is a list
    if not isinstance(events, list):
        return []

    return events
