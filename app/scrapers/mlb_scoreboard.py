# app/scrapers/mlb_scoreboard.py

import requests
from datetime import date

API_URL = "https://sports.core.api.espn.com/v2/sports/baseball/leagues/mlb/events"

def fetch_scoreboard():
    """
    Uses ESPN's new MLB events API.
    Returns a list of matchup dicts.
    """

    try:
        resp = requests.get(API_URL, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        return []

    events = data.get("items", [])
    games = []

    for event in events:
        try:
            # Fetch full event details
            event_resp = requests.get(event["$ref"], timeout=10)
            event_data = event_resp.json()

            competitions = event_data.get("competitions", [])
            if not competitions:
                continue

            comp = competitions[0]
            competitors = comp.get("competitors", [])

            home = next(c for c in competitors if c["homeAway"] == "home")
            away = next(c for c in competitors if c["homeAway"] == "away")

            # Fetch full team objects
            home_team = requests.get(home["team"]["$ref"]).json()
            away_team = requests.get(away["team"]["$ref"]).json()

            games.append({
                "game_id": event_data.get("id"),
                "game_time": event_data.get("date", "TBD"),

                "home_team": home_team.get("displayName"),
                "away_team": away_team.get("displayName"),

                "home_logo": home_team.get("logos", [{}])[0].get("href", ""),
                "away_logo": away_team.get("logos", [{}])[0].get("href", ""),

                "home_colors": {"primary": f"#{home_team.get('color', '111827')}"},
                "away_colors": {"primary": f"#{away_team.get('color', '111827')}"},

                "home_pitcher": "TBD",
                "away_pitcher": "TBD",
                "home_featured_hitter": {"name": "TBD"},
                "away_featured_hitter": {"name": "TBD"},
            })

        except Exception:
            continue

    return games
