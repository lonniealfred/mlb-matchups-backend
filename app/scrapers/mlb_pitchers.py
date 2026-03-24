# app/scrapers/mlb_pitchers.py

import requests
from bs4 import BeautifulSoup

PITCHING_URL = "https://www.espn.com/mlb/team/stats/_/type/pitching/name/{team_abbr}"

TEAM_ABBR = {
    "Yankees": "nyy",
    "Red Sox": "bos",
    "Cubs": "chc",
    "Brewers": "mil",
    "Dodgers": "lad",
    "Giants": "sf",
}

def fetch_pitchers_for_game(home_team: str, away_team: str):
    """
    Returns (home_pitcher_name, away_pitcher_name)
    Always returns "TBD" if scraping fails.
    """

    home_pitcher = scrape_team_ace(home_team)
    away_pitcher = scrape_team_ace(away_team)

    return home_pitcher, away_pitcher


def scrape_team_ace(team_name: str) -> str:
    """
    Scrapes the team's pitching stats page and returns the top pitcher.
    If anything fails → returns "TBD".
    """

    abbr = TEAM_ABBR.get(team_name)
    if not abbr:
        return "TBD"

    url = PITCHING_URL.format(team_abbr=abbr)

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except Exception:
        return "TBD"

    soup = BeautifulSoup(resp.text, "html.parser")

    # ESPN table structure: first row is usually the ace
    try:
        rows = soup.select("table tbody tr")
        if not rows:
            return "TBD"

        first_row = rows[0]
        name_cell = first_row.select_one("td:nth-of-type(1)")

        if not name_cell:
            return "TBD"

        pitcher_name = name_cell.get_text(strip=True)
        return pitcher_name or "TBD"

    except Exception:
        return "TBD"
