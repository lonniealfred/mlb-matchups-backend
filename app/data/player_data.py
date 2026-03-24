# app/data/player_data.py

import json
from pathlib import Path

# Path to the JSON file containing: { "Player Name": player_id, ... }
PLAYER_DATA_FILE = Path(__file__).parent / "player_ids.json"


def load_player_ids() -> dict:
    """
    Loads the player ID mapping from JSON.
    Returns:
        { "Aaron Judge": 33192, "Mookie Betts": 33039, ... }
    """
    try:
        if PLAYER_DATA_FILE.exists():
            with open(PLAYER_DATA_FILE, "r") as f:
                return json.load(f)
    except Exception:
        pass

    return {}  # Safe fallback


def get_player_id(name: str) -> int | None:
    """
    Returns ESPN player_id for a given player name.
    Example:
        get_player_id("Aaron Judge") -> 33192
    """
    data = load_player_ids()
    return data.get(name)


def has_player(name: str) -> bool:
    """
    Returns True if the player exists in the mapping.
    """
    data = load_player_ids()
    return name in data


def all_players() -> list:
    """
    Returns a list of all player names in the mapping.
    """
    data = load_player_ids()
    return list(data.keys())
