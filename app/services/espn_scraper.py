import requests
from datetime import datetime, timedelta

SCOREBOARD_URL = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard"
BOXSCORE_URL = "https://site.web.api.espn.com/apis/v2/sports/baseball/mlb/summary"

def fetch_scoreboard():
    res = requests.get(SCOREBOARD_URL)
    res.raise_for_status()
    return res.json()

def fetch_boxscore(game_id):
    url = f"{BOXSCORE_URL}?event={game_id}"
    res = requests.get(url)
    res.raise_for_status()
    return res.json()

def extract_pitchers(box):
    try:
        home_pitcher = box["boxscore"]["players"][0]["statistics"][0]["athletes"][0]
        away_pitcher = box["boxscore"]["players"][1]["statistics"][0]["athletes"][0]

        return {
            "home_pitcher": {
                "name": home_pitcher["athlete"]["displayName"],
                "era": float(home_pitcher.get("era", 0)),
                "whip": float(home_pitcher.get("whip", 0)),
                "hand": home_pitcher["athlete"].get("hand", "R")
            },
            "away_pitcher": {
                "name": away_pitcher["athlete"]["displayName"],
                "era": float(away_pitcher.get("era", 0)),
                "whip": float(away_pitcher.get("whip", 0)),
                "hand": away_pitcher["athlete"].get("hand", "R")
            }
        }
    except:
        return {
            "home_pitcher": None,
            "away_pitcher": None
        }

def extract_hitters(box):
    hitters = []

    try:
        for team in box["boxscore"]["players"]:
            team_abbrev = team["team"]["abbreviation"]

            for group in team["statistics"]:
                if group["name"] == "batting":
                    for athlete in group["athletes"]:
                        hitters.append({
                            "name": athlete["athlete"]["displayName"],
                            "team": team_abbrev,
                            "avg": float(athlete.get("avg", 0)),
                            "hr": int(athlete.get("hr", 0)),
                            "rbi": int(athlete.get("rbi", 0)),
                        })
    except:
        pass

    return hitters

def build_dashboard():
    data = fetch_scoreboard()

    games = []
    for event in data.get("events", []):
        game_id = event["id"]
        home = event["competitions"][0]["competitors"][0]["team"]["abbreviation"]
        away = event["competitions"][0]["competitors"][1]["team"]["abbreviation"]
        start_time = event["date"]

        box = fetch_boxscore(game_id)

        pitchers = extract_pitchers(box)
        hitters = extract_hitters(box)

        games.append({
            "game_id": game_id,
            "start_time": start_time,
            "home_team": home,
            "away_team": away,
            "pitchers": pitchers,
            "hitters": hitters
        })

    return {"games": games}
