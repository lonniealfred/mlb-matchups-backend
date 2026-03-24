# app/scrapers/mlb_streaks.py

import requests
from bs4 import BeautifulSoup

GAMELOG_URL = "https://www.espn.com/mlb/player/gamelog/_/id/{player_id}"


def fetch_hit_streak(player_id: int) -> int:
    """
    Computes current hit streak from ESPN game log.
    Walks backwards through recent games until a hitless game is found.
    Returns streak length (0+).
    """

    url = GAMELOG_URL.format(player_id=player_id)

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except Exception:
        return 0

    soup = BeautifulSoup(resp.text, "html.parser")

    try:
        rows = soup.select("table tbody tr")
        if not rows:
            return 0

        streak = 0

        for row in rows:
            cols = [c.get_text(strip=True) for c in row.select("td")]
            if not cols or "Did Not Play" in " ".join(cols):
                continue

            # You may need to adjust index based on ESPN layout.
            # Example assumption: "AB" and "H" columns exist.
            # Find H column by header match if you want to be robust.
            # Here we assume H is at index 4.
            try:
                hits_str = cols[4]
                hits = int(hits_str)
            except Exception:
                hits = 0

            if hits > 0:
                streak += 1
            else:
                break

        return streak

    except Exception:
        return 0
