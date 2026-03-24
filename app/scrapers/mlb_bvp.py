# app/scrapers/mlb_bvp.py

import requests
from bs4 import BeautifulSoup

BVP_URL = "https://www.espn.com/mlb/player/batvspitch/_/id/{hitter_id}/pitcherId/{pitcher_id}"


def fetch_bvp(hitter_id: int, pitcher_id: int) -> dict:
    """
    Fetches batter-vs-pitcher stats from ESPN.
    Returns:
    {
      "bvp_hrs": int,
      "bvp_avg": float
    }
    Falls back to zeros on any failure.
    """

    url = BVP_URL.format(hitter_id=hitter_id, pitcher_id=pitcher_id)

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except Exception:
        return {"bvp_hrs": 0, "bvp_avg": 0.000}

    soup = BeautifulSoup(resp.text, "html.parser")

    try:
        # ESPN usually has a table with BvP stats; first row is aggregate
        row = soup.select_one("table tbody tr")
        if not row:
            return {"bvp_hrs": 0, "bvp_avg": 0.000}

        cols = [c.get_text(strip=True) for c in row.select("td")]
        # You may need to adjust indices based on ESPN layout
        # Example assumption:
        # cols[1] = AB, cols[2] = H, cols[3] = AVG, cols[6] = HR
        avg_str = cols[3] if len(cols) > 3 else ".000"
        hr_str = cols[6] if len(cols) > 6 else "0"

        try:
            bvp_avg = float(avg_str)
        except Exception:
            bvp_avg = 0.000

        try:
            bvp_hrs = int(hr_str)
        except Exception:
            bvp_hrs = 0

        return {"bvp_hrs": bvp_hrs, "bvp_avg": bvp_avg}

    except Exception:
        return {"bvp_hrs": 0, "bvp_avg": 0.000}
