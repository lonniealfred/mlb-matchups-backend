import requests
from typing import List, Dict, Any

# ---------------------------------------------------------
# ESPN ENDPOINTS (current, working)
# ---------------------------------------------------------

SCOREBOARD_URL = "https://sports.core.api.espn.com/v2/sports/baseball/leagues/mlb/events"
SUMMARY_URL = "https://sports.core.api.espn.com/v2/sports/baseball/leagues/mlb/events/{event_id}/competitions/{event_id}/details"


# ---------------------------------------------------------
# 1. Fetch MLB scoreboard (list of event IDs)
# ---------------------------------------------------------

def get_scoreboard() -> Dict[str, Any]:
    resp = requests.get(SCOREBOARD_URL, timeout=10)

    if resp.status_code != 200:
        print(f"Scoreboard fetch failed: {resp.status_code}")
        return {"items": []}

    return resp.json()


# ---------------------------------------------------------
# 2. Extract event IDs from scoreboard
# ---------------------------------------------------------

def extract_event_ids(scoreboard: Dict[str, Any]) -> List[str]:
    items = scoreboard.get("items", [])
    event_ids = []

    for item in items:
        # ESPN returns event URLs like:
        # https://sports.core.api.espn.com/v2/sports/baseball/leagues/mlb/events/401559123
        href = item.get("$ref")
        if not href:
            continue

        event_id = href.rstrip("/").split("/")[-1]
        event_ids.append(event_id)

    return event_ids


# ---------------------------------------------------------
# 3. Fetch boxscore/summary for a specific event
# ---------------------------------------------------------

def get_boxscore(event_id: str) -> Dict[str, Any]:
    url = SUMMARY_URL.format(event_id=event_id)
    resp = requests.get(url, timeout=10)

    if resp.status_code != 200:
        print(f"Boxscore fetch failed for {event_id}: {resp.status_code}")
        return {}

    return resp.json()


# ---------------------------------------------------------
# 4. Extract teams + hitters from ESPN summary
# ---------------------------------------------------------

def extract_game_data(event_id: str, summary: Dict[str, Any]) -> Dict[str, Any]:
    competitions = summary.get("competitions", [])
    if not competitions:
        return None

    comp = competitions[0]

    competitors = comp.get("competitors", [])
    if len(competitors) < 2:
        return None

    away = next((c for c in competitors if c.get("homeAway") == "away"), None)
    home = next((c for c in competitors if c.get("homeAway") == "home"), None)

    if not away or not home:
        return None

    away_team = away["team"]["abbreviation"]
    home_team = home["team"]["abbreviation"]

    # Hitters come from "statistics" → "athletes"
    stats = comp.get("statistics", [])
    batting_stats = next((s for s in stats if s.get("name") == "batting"), None)

    if not batting_stats:
        return {
            "game_id": event_id,
            "away_team": away_team,
            "home_team": home_team,
            "hitters": {
                "has_boxscore": False,
                "away_top_hitters": [],
                "home_top_hitters": []
            }
        }

    athletes = batting_stats.get("athletes", [])
    if not athletes:
        return {
            "game_id": event_id,
            "away_team": away_team,
            "home_team": home_team,
            "hitters": {
                "has_boxscore": False,
                "away_top_hitters": [],
                "home_top_hitters": []
            }
        }

    away_hitters = []
    home_hitters = []

    for entry in athletes:
        athlete = entry.get("athlete", {})
        team = entry.get("team", {})
        team_abbr = team.get("abbreviation")

        hitter = {
            "id": athlete.get("id"),
            "name": athlete.get("displayName"),
            "hitter_score": 10,
            "streak": 0,
        }

        if team_abbr == away_team:
            away_hitters.append(hitter)
        elif team_abbr == home_team:
            home_hitters.append(hitter)

    return {
        "game_id": event_id,
        "away_team": away_team,
        "home_team": home_team,
        "hitters": {
            "has_boxscore": True,
            "away_top_hitters": away_hitters[:9],
            "home_top_hitters": home_hitters[:9]
        }
    }


# ---------------------------------------------------------
# 5. Main function used by /dashboard
# ---------------------------------------------------------

def get_mlb_games_with_hitters() -> List[Dict[str, Any]]:
    print(">>> ESPN SCRAPER IS RUNNING <<<")

    scoreboard = get_scoreboard()
    event_ids = extract_event_ids(scoreboard)

    games = []

    for event_id in event_ids:
        summary = get_boxscore(event_id)

        if not summary:
            continue

        game_data = extract_game_data(event_id, summary)

        if game_data:
            games.append(game_data)

    return games
