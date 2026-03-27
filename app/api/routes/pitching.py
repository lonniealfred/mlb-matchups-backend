from fastapi import APIRouter
from app.scrapers.mlb_scoreboard import fetch_scoreboard
from app.scrapers.mlb_pitchers import fetch_pitchers_for_game

router = APIRouter()

@router.get("/pitching")
def get_pitching():
    try:
        scoreboard = fetch_scoreboard()
        events = scoreboard.get("events", [])

        pitchers = []

        for game in events:
            competitions = game.get("competitions", [])
            if not competitions:
                continue

            comp = competitions[0]
            competitors = comp.get("competitors", [])
            if len(competitors) != 2:
                continue

            # Identify home/away
            home = competitors[0] if competitors[0].get("homeAway") == "home" else competitors[1]
            away = competitors[1] if home is competitors[0] else competitors[0]

            home_team = home.get("team", {}).get("displayName", "Unknown")
            away_team = away.get("team", {}).get("displayName", "Unknown")

            # Scrape pitchers for this matchup
            home_pitcher, away_pitcher = fetch_pitchers_for_game(home_team, away_team)

            pitchers.append({
                "home_team": home_team,
                "away_team": away_team,
                "home_pitcher": home_pitcher,
                "away_pitcher": away_pitcher
            })

        return {
            "status": "ok",
            "pitchers": pitchers,
            "message": ""
        }

    except Exception as e:
        return {
            "status": "error",
            "pitchers": [],
            "message": f"Failed to load pitching data: {e}"
        }
