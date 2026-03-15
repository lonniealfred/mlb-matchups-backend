import requests
from typing import List, Dict, Any

SCOREBOARD_URL = "https://site.web.api.espn.com/apis/v2/sports/baseball/mlb/scoreboard"
BOX_URL_TEMPLATE = "https://site.web.api.espn.com/apis/v2/sports/baseball/mlb/summary?event={event_id}"


def get_scoreboard() -> Dict[str, Any]:
    resp = requests.get(SCOREBOARD_URL, timeout=10)
    resp.raise_for_status()
    return resp.json()


def extract_games(scoreboard: Dict[str, Any]) -> List[Dict[str, Any]]:
    events = scoreboard.get("events", [])
    games = []

    for ev in events:
        event_id = ev.get("id")
        competitions = ev.get("competitions", [])
        if not competitions:
            continue

        comp = competitions[0]
        competitors = comp.get("competitors", [])

        away = next((c for c in competitors if c.get("homeAway") == "away"), None)
        home = next((c for c in competitors if c.get("homeAway") == "home"), None)

        if not away or not home:
            continue

        games.append({
            "event_id": event_id,
            "game_id": event_id,
            "away_team": away["team"]["abbreviation"],
            "home_team": home["team"]["abbreviation"],
            "start_time": ev.get("date"),
        })

    return games


def get_boxscore(event_id: str) -> Dict[str, Any]:
    url = BOX_URL_TEMPLATE.format(event_id=event_id)
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json()


def extract_hitters_from_box(box: Dict[str, Any], away_abbr: str, home_abbr: str) -> Dict[str, Any]:
    boxscore = box.get("boxscore")
    if not boxscore:
        return {"has_boxscore": False, "away_top_hitters": [], "home_top_hitters": []}

    players_groups = boxscore.get("players")
    if not players_groups:
        return {"has_boxscore": False, "away_top_hitters": [], "home_top_hitters": []}

    away_hitters = []
    home_hitters = []

    for group in players_groups:
        team = group.get("team", {})
        team_abbr = team.get("abbreviation")
        stats = group.get("statistics", [])

        batting = next((s for s in stats if s.get("name") == "batting"), None)
        if not batting:
            continue

        athletes = batting.get("athletes", [])
        if not athletes:
            continue

        for athlete in athletes:
            ath = athlete.get("athlete", {})
            name = ath.get("displayName")
            athlete_id = ath.get("id")

            hitter = {
                "id": athlete_id,
                "name": name,
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
        "home_top_hitters": home_hitters[:9],
    }


def get_mlb_games_with_hitters() -> List[Dict[str, Any]]:
    print(">>> ESPN SCRAPER IS RUNNING <<<")

    scoreboard = get_scoreboard()
    games = extract_games(scoreboard)

    enriched_games = []
    for g in games:
        try:
            box = get_boxscore(g["event_id"])
            hitters = extract_hitters_from_box(box, g["away_team"], g["home_team"])
        except Exception as e:
            print(f"Boxscore error for event {g['event_id']}: {e}")
            hitters = {
                "has_boxscore": False,
                "away_top_hitters": [],
                "home_top_hitters": []
            }

        enriched_games.append({
            **g,
            "hitters": hitters,
        })

    return enriched_games
