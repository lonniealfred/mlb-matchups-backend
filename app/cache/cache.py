# app/cache/cache.py

import json
import os
from datetime import datetime, timedelta
from typing import Any, Optional

from app.config import settings


CACHE_PATH = "app/cache/espn_cache.json"
CACHE_TTL_MINUTES = 5  # how long cached data stays fresh


# ---------------------------------------------------------
# Ensure cache file exists
# ---------------------------------------------------------

def _ensure_cache_file():
    if not os.path.exists(CACHE_PATH):
        os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
        with open(CACHE_PATH, "w") as f:
            json.dump({
                "scoreboard": {"timestamp": None, "data": {}},
                "player_stats": {"timestamp": None, "data": {}},
                "venue": {"timestamp": None, "data": {}},
                "bvp": {"timestamp": None, "data": {}},
                "hit_streak": {"timestamp": None, "data": {}}
            }, f, indent=2)


# ---------------------------------------------------------
# Load / Save cache
# ---------------------------------------------------------

def _load_cache() -> dict:
    _ensure_cache_file()
    with open(CACHE_PATH, "r") as f:
        return json.load(f)


def _save_cache(cache: dict):
    with open(CACHE_PATH, "w") as f:
        json.dump(cache, f, indent=2)


# ---------------------------------------------------------
# Expiration logic
# ---------------------------------------------------------

def _is_fresh(timestamp: Optional[str]) -> bool:
    if not timestamp:
        return False
    try:
        ts = datetime.fromisoformat(timestamp)
        return datetime.now() - ts < timedelta(minutes=CACHE_TTL_MINUTES)
    except Exception:
        return False


# ---------------------------------------------------------
# Public API
# ---------------------------------------------------------

def get_cached(endpoint: str, key: str = None) -> Optional[Any]:
    """
    Returns cached data for a given endpoint.
    If key is provided (e.g., player_id), returns nested entry.
    """
    if not settings.enable_scraper_cache:
        return None

    cache = _load_cache()
    entry = cache.get(endpoint)

    if not entry or not _is_fresh(entry["timestamp"]):
        return None

    if key:
        return entry["data"].get(key)

    return entry["data"]


def set_cached(endpoint: str, data: Any, key: str = None):
    """
    Writes data to cache for a given endpoint.
    If key is provided, stores under nested key.
    """
    if not settings.enable_scraper_cache:
        return

    cache = _load_cache()

    if endpoint not in cache:
        cache[endpoint] = {"timestamp": None, "data": {}}

    cache[endpoint]["timestamp"] = datetime.now().isoformat()

    if key:
        cache[endpoint]["data"][key] = data
    else:
        cache[endpoint]["data"] = data

    _save_cache(cache)
