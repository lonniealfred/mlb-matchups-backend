# app/scrapers/mlb_scoreboard.py

import requests
from bs4 import BeautifulSoup
from datetime import date

SCOREBOARD_URL = "https://www.espn.com/mlb/scoreboard/_/date/{date_str}"

# Optional: team logo + color mapping
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


def fetch_scoreboard():
    """
    Scrapes ESPN's MLB scoreboard for today's games.
    Returns a list of matchup dicts.
    If ESPN returns no games (offseason, rainouts, etc),
    returns an empty list — your dashboard_live will fill with TBD defaults.
    """

    today = date.today().strftime("%Y%m%d")
    url = SCOREBOARD_URL.format(date_str=today)

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except Exception:
        # If ESPN is unreachable → return empty list
        return []

    soup = BeautifulSoup(resp.text, "html.parser")

    games = []

    # ESPN Scoreboard structure
    scoreboard_games = soup.select(".Scoreboard")

    if not scoreboard_games:
        # No games today (offseason or ESPN changed layout)
        return []

    for game in scoreboard_games:
        try:
            home_team_el = game.select_one(".ScoreCell__Team--home .ScoreCell__TeamName")
            away_team_el = game.select_one(".ScoreCell__Team--away .ScoreCell__TeamName")
            time_el = game.select_one(".ScoreCell__Time")

            home_team = home_team_el.get_text(strip=True) if home_team_el else "TBD"
            away_team = away_team_el.get_text(strip=True) if away_team_el else "TBD"
            game_time = time_el.get_text(strip=True) if time_el else "TBD"

            games.append({
                "game_id": f"{home_team}-{away_team}",
                "home_team": home_team,
                "away_team": away_team,
                "game_time": game_time,

                # Logos + colors (fallback to neutral)
                "home_logo": TEAM_LOGOS.get(home_team, ""),
                "away_logo": TEAM_LOGOS.get(away_team, ""),
                "home_colors": TEAM_COLORS.get(home_team, {"primary": "#111827"}),
                "away_colors": TEAM_COLORS.get(away_team, {"primary": "#111827"}),

                # Pitchers + hitters will be filled by dashboard_live
                "home_pitcher": "TBD",
                "away_pitcher": "TBD",
                "home_featured_hitter": {"name": "TBD", "avg": ".---", "hr": 0},
                "away_featured_hitter": {"name": "TBD", "avg": ".---", "hr": 0},
            })

        except Exception:
            # If any parsing fails, skip this game safely
            continue

    return games
