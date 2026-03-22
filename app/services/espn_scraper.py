# app/services/espn_scraper.py

import httpx
from typing import Dict, Any, List, Optional
from app.services.analytics import (
    calculate_pitcher_difficulty,
    calculate_hitter_difficulty,
)

ESPN_SCOREBOARD = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard"
ESPN_BOXSCORE = "https://site.web.api.espn.com/apis/v2/sports/baseball/mlb/summary"


async def fetch_json(url: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict]:
    """Safe JSON fetch with timeout + fallback."""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(url, params=params)
            if r.status_code == 200:
                return r.json()
    except Exception as e:
        print("Fetch error:", e)
    return None


async def fetch_scoreboard() -> Optional[Dict]:
    return await fetch_json(ESPN_SCOREBOARD)


async def fetch_boxscore(game_id: str) -> Optional[Dict]:
    return await fetch_json(ESPN_BOXSCORE, params={"event": game_id})


def extract_pitcher(stats: Dict[str, Any]) -> Dict[str, Any]:
    """Extract pitcher stats safely."""
    return {
        "name": stats.get("athlete", {}).get("displayName", "Unknown Pitcher"),
        "era": float(stats.get("era", 4.00)),
        "whip": float(stats.get("whip", 1.30)),
        "k9": float(stats.get("k9", 8.0)),
        "bb9": float(stats.get("bb9", 2.5)),
        "opp_avg": float(stats.get("opponentBattingAvg", 0.250)),
        "team": stats.get("team", "Unknown"),
    }


def extract_hitter(stats: Dict[str, Any]) -> Dict[str, Any]:
    """Extract hitter stats safely."""
    return {
        "name": stats.get("athlete", {}).get("displayName", "Unknown Hitter"),
        "avg": float(stats.get("avg", 0.250)),
        "hr": int(stats.get("hr", 0)),
        "rbi": int(stats.get("rbi", 0)),
        "ops": float(stats.get("ops", 0.700)),
        "team": stats.get("team", "Unknown"),
        "hit_streak": int(stats.get("hitStreak", 0)),
    }


async def build_dashboard() -> Dict[str, Any]:
    """
    Main scraper entry point.
    Returns:
      - matchups[]
      - pitchers[]
      - hitters[]
    """

    scoreboard = await fetch_scoreboard()
    if not scoreboard or "events" not in scoreboard:
        print("Scoreboard unavailable — returning None")
        return None

    matchups: List[Dict[str, Any]] = []
    pitchers: List[Dict[str, Any]] = []
    hitters: List[Dict[str, Any]] = []

    for event in scoreboard["events"]:
        try:
            game_id = event.get("id")
            competitions = event.get("competitions", [])
            if not competitions:
                continue

            comp = competitions[0]
            teams = comp.get("competitors", [])

            home = next((t for t in teams if t.get("homeAway") == "home"), None)
            away = next((t for t in teams if t.get("homeAway") == "away"), None)

            if not home or not away:
                continue

            # Basic matchup info
            home_team = home.get("team", {}).get("displayName", "Home")
            away_team = away.get("team", {}).get("displayName", "Away")
            home_logo = home.get("team", {}).get("logo")
            away_logo = away.get("team", {}).get("logo")
            venue = comp.get("venue", {}).get("fullName", "Unknown Venue")
            start_time = event.get("date")

            # Weather (fallback-safe)
            weather = comp.get("weather", {})
            temp_f = weather.get("temperature", 70)
            condition = weather.get("displayValue", "Clear")
            wind_mph = weather.get("windSpeed", 5)

            # Stadium + analytics placeholders
            park_factor = 1.05
            weather_factor = 1.02
            momentum_rating = 0.6
            opp_lineup_ops = 0.720
            opp_hot_streaks = 1

            # Fetch boxscore
            box = await fetch_boxscore(game_id)
            if not box:
                continue

            # Extract pitchers
            home_pitcher_raw = (
                box.get("boxscore", {})
                .get("players", [{}])[0]
                .get("statistics", [{}])[0]
            )
            away_pitcher_raw = (
                box.get("boxscore", {})
                .get("players", [{}])[1]
                .get("statistics", [{}])[0]
            )

            home_pitcher = extract_pitcher(home_pitcher_raw)
            away_pitcher = extract_pitcher(away_pitcher_raw)

            # Difficulty scoring context
            context = {
                "park_factor": park_factor,
                "weather_factor": weather_factor,
                "momentum_rating": momentum_rating,
                "opp_lineup_ops": opp_lineup_ops,
                "opp_hot_streaks": opp_hot_streaks,
            }

            home_pitcher["difficulty"] = calculate_pitcher_difficulty(home_pitcher, context)
            away_pitcher["difficulty"] = calculate_pitcher_difficulty(away_pitcher, context)

            pitchers.append(home_pitcher)
            pitchers.append(away_pitcher)

            # Extract hitters
            hitters_raw = box.get("boxscore", {}).get("players", [])
            for team_block in hitters_raw:
                for stat in team_block.get("statistics", []):
                    h = extract_hitter(stat)
                    h["difficulty"] = calculate_hitter_difficulty(h, context)
                    hitters.append(h)

            # Build matchup object
            matchups.append({
                "home_team": home_team,
                "away_team": away_team,
                "home_logo": home_logo,
                "away_logo": away_logo,
                "start_time": start_time,
                "venue": venue,
                "weather": {
                    "temp_f": temp_f,
                    "condition": condition,
                    "wind_mph": wind_mph,
                },
                "analytics": {
                    "run_expectancy": 8.5,
                    "park_factor": park_factor,
                    "weather_factor": weather_factor,
                    "momentum_rating": momentum_rating,
                },
                "home_pitcher": home_pitcher,
                "away_pitcher": away_pitcher,
            })

        except Exception as e:
            print("Error building matchup:", e)
            continue

    return {
        "matchups": matchups,
        "pitchers": pitchers,
        "hitters": hitters,
        "status": "live",
    }
