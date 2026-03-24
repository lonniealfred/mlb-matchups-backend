# app/services/http_cache.py

import time
import requests
from typing import Optional, Dict, Tuple

# url -> (expires_at, response_text)
_CACHE: Dict[str, Tuple[float, str]] = {}

DEFAULT_TTL = 120  # 2 minutes; adjust as needed


def cached_get(url: str, ttl: int = DEFAULT_TTL) -> Optional[str]:
    """
    Cached HTTP GET.
    - Returns cached response if not expired
    - Otherwise fetches, stores, and returns
    - Returns None on failure
    """

    now = time.time()

    # Serve from cache
    if url in _CACHE:
        expires_at, text = _CACHE[url]
        if now < expires_at:
            return text

    # Fetch fresh
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        text = resp.text
        _CACHE[url] = (now + ttl, text)
        return text
    except Exception:
        return None
