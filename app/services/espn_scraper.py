import requests
from typing import Dict, Any, List

SCOREBOARD_URL = "https://sports.core.api.espn.com/v2/sports/baseball/leagues/mlb/events"


def safe_get(url: str) -> Dict[str, Any]:
    """Fetch JSON safely without crashing."""
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            print(f"Fetch failed {r.status_code}: {url}")
            return {}
        return r.json()
    except Exception as e:
        print(f"Request error for {url}: {e}")
        return {}


# ---------------------------------------------------------
# 1. Fetch event IDs
# ---------------------------------------------------------

def get_event_ids() -> List[str]:
    data = safe_get(SCOREBOARD_URL)
    items = data.get("items", [])
    event_ids = []

    for item in items:
        href = item.get("$ref")
        if not href:
            continue
        event_id = href.rstrip("/").split("/")[-1]
        event_ids.append(event_id)

    return event_ids


# ---------------------------------------------------------
# 2. Fetch competition summary
# ---------------------------------------------------------

def get_summary(event_id: str) -> Dict[str, Any]:
    url = f"https://sports.core.api.espn.com/v2/sports/baseball/leagues/mlb/events/{event_id}/competitions/{event_id}/details"
    return safe_get(url)


# ---------------------------------------------------------
# 3. Resolve team abbreviation from ESPN team URL
# ---------------------------------------------------------

def resolve_team_abbr(team_ref: str) -> str:
    team_data = safe_get(team_ref)
    return team_data.get("abbreviation", "UNK")


# ---------------------------------------------------------
# 4. Extract hitters safely
# ---------------------------------------------------------

def extract_hitters(summary: Dict[str, Any], away_abbr: str, home_abbr: str) -> Dict[str, Any]:
    stats = summary.get("statistics", [])
    batting = next((s for s in stats if s.get("name") == "batting"), None)

    if not batting:
        return {
            "has_boxscore": False,
            "away_top_hitters": [],
            "home_top_hitters": []
        }

    athletes = batting.get("athletes", [])
    if not athletes:
        return {
            "has_boxscore": False,
            "away_top_hitters": [],
            "home_top_hitters": []
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

        if team_abbr == away_abbr:
            away_hitters.append(hitter)
        elif team_abbr == home_abbr:
            home_hitters.append(hitter)

    return {
        "has_boxscore": True,
        "away_top_hitters": away_hitters[:9],
        "home_top_hitters": home_hitters[:9]
    }


# ---------------------------------------------------------
# 5. Main function used by /dashboard
# ---------------------------------------------------------

def get_mlb_games_with_hitters() -> List[Dict[str, Any]]:
    print(">>> ESPN SCRAPER IS RUNNING <<<")

    event_ids = get_event_ids()
    games = []

    for event_id in event_ids:
        summary = get_summary(event_id)
        if not summary:
            continue

        competitions = summary.get("competitions", [])
        if not competitions:
            continue

        comp = competitions[0]
        competitors = comp.get("competitors", [])
        if len(competitors) < 2:
            continue

        away = next((c for c in competitors if c.get("homeAway") == "away"), None)
        home = next((c for c in competitors if c.get("homeAway") == "home"), None)

        if not away or not home:
            continue

        # Resolve team abbreviations from ESPN team URLs
        away_abbr = resolve_team_abbr(away["team"]["$ref"])
        home_abbr = resolve_team_abbr(home["team"]["$ref"])

        hitters = extract_hitters(summary, away_abbr, home_abbr)

        games.append({
            "game_id": event_id,
            "away_team": away_abbr,
            "home_team": home_abbr,
            "hitters": hitters
        })

    return games
