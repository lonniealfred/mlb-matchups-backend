# app/scrapers/mlb_season_stats.py

import requests
from bs4 import BeautifulSoup

SEASON_STATS_URL = "https://www.espn.com/mlb/player/stats/_/id/{player_id}"


def fetch_season_stats(player_id: int) -> dict:
    """
    Fetches season AVG and HR from ESPN player stats.
    Returns:
    {
      "avg": float,
      "hr": int
    }
    Falls back to .000 and 0 on failure.
    """

    url = SEASON_STATS_URL.format(player_id=player_id)

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except Exception:
        return {"avg": 0.000, "hr": 0}

    soup = BeautifulSoup(resp.text, "html.parser")

    try:
        # ESPN usually has a "Batting" stats table; last row is season total
        rows = soup.select("table tbody tr")
        if not rows:
            return {"avg": 0.000, "hr": 0}

        last_row = rows[-1]
        cols = [c.get_text(strip=True) for c in last_row.select("td")]

        # You may need to adjust indices based on ESPN layout.
        # Example assumption:
        # AVG at index 9, HR at index 6.
        avg_str = cols[9] if len(cols) > 9 else ".000"
        hr_str = cols[6] if len(cols) > 6 else "0"

        try:
            avg = float(avg_str)
        except Exception:
            avg = 0.000

        try:
            hr = int(hr_str)
        except Exception:
            hr = 0

        return {"avg": avg, "hr": hr}

    except Exception:
        return {"avg": 0.000, "hr": 0}
