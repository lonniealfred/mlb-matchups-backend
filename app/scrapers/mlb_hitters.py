# app/scrapers/mlb_hitters.py

import requests
from bs4 import BeautifulSoup

TEAM_ABBR = {
    "Yankees": "nyy",
    "Red Sox": "bos",
    "Cubs": "chc",
    "Brewers": "mil",
    "Dodgers": "lad",
    "Giants": "sf",
}

TEAM_LOGOS = {
    "Yankees": "https://a.espncdn.com/i/teamlogos/mlb/500/nyy.png",
    "Red Sox": "https://a.espncdn.com/i/teamlogos/mlb/500/bos.png",
    "Cubs": "https://a.espncdn.com/i/teamlogos/mlb/500/chc.png",
    "Brewers": "https://a.espncdn.com/i/teamlogos/mlb/500/mil.png",
    "Dodgers": "https://a.espncdn.com/i/teamlogos/mlb/500/lad.png",
    "Giants": "https://a.espncdn.com/i/teamlogos/mlb/500/sf.png",
}

TEAM_COLORS = {
    "Yankees": {"primary": "#132448"},
    "Red Sox": {"primary": "#BD3039"},
    "Cubs": {"primary": "#0E3386"},
    "Brewers": {"primary": "#12284B"},
    "Dodgers": {"primary": "#005A9C"},
    "Giants": {"primary": "#FD5A1E"},
}

HITTING_URL = "https://www.espn.com/mlb/team/stats/_/type/batting/name/{team_abbr}"


def fetch_featured_hitters(home_team: str, away_team: str, leaderboard: bool = False):
    """
    If leaderboard=True → returns a league-wide hitters list (empty for now).
    Otherwise → returns (home_featured_hitter, away_featured_hitter).
    Always returns safe defaults when scraping fails.
    """

    if leaderboard:
        # Placeholder until you add scoring logic
        return []

    home = scrape_team_top_hitter(home_team)
    away = scrape_team_top_hitter(away_team)

    return home, away


def scrape_team_top_hitter(team_name: str):
    """
    Scrapes ESPN batting stats for a team and returns the top hitter.
    If anything fails → returns a safe TBD hitter object.
    """

    abbr = TEAM_ABBR.get(team_name)
    if not abbr:
        return default_hitter(team_name)

    url = HITTING_URL.format(team_abbr=abbr)

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except Exception:
        return default_hitter(team_name)

    soup = BeautifulSoup(resp.text, "html.parser")

    try:
        rows = soup.select("table tbody tr")
        if not rows:
            return default_hitter(team_name)

        first_row = rows[0]
        cols = [c.get_text(strip=True) for c in first_row.select("td")]

        if len(cols) < 7:
            return default_hitter(team_name)

        name = cols[0]
        avg = cols[5] if cols[5] else ".---"
        hr = cols[6] if cols[6].isdigit() else "0"

        return {
            "name": name,
            "avg": avg,
            "hr": int(hr),
            "team": team_name,
            "logo": TEAM_LOGOS.get(team_name, ""),
            "colors": TEAM_COLORS.get(team_name, {"primary": "#111827"}),
        }

    except Exception:
        return default_hitter(team_name)


def default_hitter(team_name: str):
    """
    Returns a safe fallback hitter object.
    """

    return {
        "name": "TBD",
        "avg": ".---",
        "hr": 0,
        "team": team_name,
        "logo": TEAM_LOGOS.get(team_name, ""),
        "colors": TEAM_COLORS.get(team_name, {"primary": "#111827"}),
    }
