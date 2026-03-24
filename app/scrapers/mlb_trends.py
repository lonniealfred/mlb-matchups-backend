# app/scrapers/mlb_trends.py

import requests
from bs4 import BeautifulSoup

STADIUM_FACTORS_URL = "https://www.espn.com/mlb/stats/team/_/stat/batting/table/homeruns"
WEATHER_URL = "https://www.espn.com/mlb/scoreboard"
STANDINGS_URL = "https://www.espn.com/mlb/standings"


def fetch_trends():
    """
    Returns a dict containing:
    - stadium_factors
    - weather_factors
    - momentum
    - league_scoring_trends
    - team_streaks

    Every section is wrapped in try/except so the dashboard never breaks.
    """

    return {
        "stadium_factors": safe_fetch(fetch_stadium_factors, []),
        "weather_factors": safe_fetch(fetch_weather_factors, []),
        "momentum": safe_fetch(fetch_team_momentum, []),
        "league_scoring_trends": safe_fetch(fetch_league_scoring, {}),
        "team_streaks": safe_fetch(fetch_team_streaks, []),
    }


def safe_fetch(func, fallback):
    """Runs a scraper function safely and returns fallback on failure."""
    try:
        data = func()
        return data if data else fallback
    except Exception:
        return fallback


# ------------------------------------------------------------
# 1. Stadium HR Factors
# ------------------------------------------------------------

def fetch_stadium_factors():
    """
    Scrapes ESPN's HR factor table.
    Returns: [{ stadium, hr_factor }]
    """

    try:
        resp = requests.get(STADIUM_FACTORS_URL, timeout=10)
        resp.raise_for_status()
    except Exception:
        return []

    soup = BeautifulSoup(resp.text, "html.parser")

    rows = soup.select("table tbody tr")
    if not rows:
        return []

    factors = []

    for row in rows[:10]:  # top 10 stadiums
        cols = [c.get_text(strip=True) for c in row.select("td")]
        if len(cols) < 3:
            continue

        stadium = cols[1]
        hr_factor = cols[2]

        try:
            hr_factor = float(hr_factor)
        except:
            hr_factor = None

        factors.append({
            "stadium": stadium,
            "hr_factor": hr_factor
        })

    return factors


# ------------------------------------------------------------
# 2. Weather Factors (very light placeholder)
# ------------------------------------------------------------

def fetch_weather_factors():
    """
    Placeholder: returns empty list.
    Later you can integrate a real weather API (OpenWeather, MLB WeatherEdge).
    """

    return []


# ------------------------------------------------------------
# 3. Team Momentum (from standings)
# ------------------------------------------------------------

def fetch_team_momentum():
    """
    Scrapes ESPN standings to extract last-10 records.
    Returns: [{ team, trend }]
    """

    try:
        resp = requests.get(STANDINGS_URL, timeout=10)
        resp.raise_for_status()
    except Exception:
        return []

    soup = BeautifulSoup(resp.text, "html.parser")

    rows = soup.select("table tbody tr")
    if not rows:
        return []

    momentum = []

    for row in rows:
        cols = [c.get_text(strip=True) for c in row.select("td")]
        if len(cols) < 10:
            continue

        team = cols[0]
        last10 = cols[-2]  # ESPN usually puts L10 near the end

        momentum.append({
            "team": team,
            "trend": f"L10: {last10}"
        })

    return momentum


# ------------------------------------------------------------
# 4. League Scoring Trends (placeholder)
# ------------------------------------------------------------

def fetch_league_scoring():
    """
    Placeholder: returns static scoring trends.
    Later you can scrape ESPN league stats or Statcast.
    """

    return {
        "runs_per_game": 9.1,
        "hr_per_game": 2.3
    }


# ------------------------------------------------------------
# 5. Team Streaks (from standings)
# ------------------------------------------------------------

def fetch_team_streaks():
    """
    Scrapes ESPN standings to extract streaks.
    Returns: [{ team, streak }]
    """

    try:
        resp = requests.get(STANDINGS_URL, timeout=10)
        resp.raise_for_status()
    except Exception:
        return []

    soup = BeautifulSoup(resp.text, "html.parser")

    rows = soup.select("table tbody tr")
    if not rows:
        return []

    streaks = []

    for row in rows:
        cols = [c.get_text(strip=True) for c in row.select("td")]
        if len(cols) < 10:
            continue

        team = cols[0]
        streak = cols[-1]  # ESPN usually puts streak at the end

        streaks.append({
            "team": team,
            "streak": streak
        })

    return streaks
