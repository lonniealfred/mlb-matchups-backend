# app/services/dashboard_live.py

from app.scrapers.mlb_scoreboard import fetch_scoreboard
from app.scrapers.mlb_pitchers import fetch_pitchers_for_game
from app.scrapers.mlb_hitters import fetch_featured_hitters
from app.scrapers.mlb_trends import fetch_trends

from app.services.hitters_leaderboard import build_hitters_leaderboard


def build_live_dashboard():
    """
    Builds the full live dashboard payload.
    - Scrapes scoreboard, pitchers, hitters, trends
    - Builds full hitters leaderboard (BvP + streak + season stats + scoring)
    - Inserts TBD defaults when data is missing
    - Never throws errors (dashboard always loads)
    """

    # -----------------------------
    # 1. SCOREBOARD (games list)
    # -----------------------------
    try:
        games = fetch_scoreboard()
    except Exception:
        games = []

    matchups = []
    pitchers_list = []

    # -----------------------------
    # 2. PROCESS EACH GAME
    # -----------------------------
    for g in games:
        home = g.get("home_team", "TBD")
        away = g.get("away_team", "TBD")

        # -----------------------------
        # Pitchers
        # -----------------------------
        try:
            home_pitcher, away_pitcher = fetch_pitchers_for_game(home, away)
        except Exception:
            home_pitcher, away_pitcher = "TBD", "TBD"

        # -----------------------------
        # Featured Hitters (names only)
        # -----------------------------
        try:
            home_hitter, away_hitter = fetch_featured_hitters(home, away)
        except Exception:
            home_hitter = {"name": "TBD", "team": home}
            away_hitter = {"name": "TBD", "team": away}

        # -----------------------------
        # Build matchup object
        # -----------------------------
        matchups.append({
            "game_id": g.get("game_id", f"{home}-{away}"),
            "home_team": home,
            "away_team": away,
            "home_logo": g.get("home_logo", ""),
            "away_logo": g.get("away_logo", ""),
            "home_featured_hitter": home_hitter,
            "away_featured_hitter": away_hitter,
            "home_pitcher": home_pitcher,
            "away_pitcher": away_pitcher,
            "game_time": g.get("game_time", "TBD"),
            "home_colors": g.get("home_colors", {"primary": "#111827"}),
            "away_colors": g.get("away_colors", {"primary": "#111827"}),
        })

        # -----------------------------
        # Pitchers list for Pitchers tab
        # -----------------------------
        if home_pitcher != "TBD":
            pitchers_list.append({
                "name": home_pitcher,
                "team": home,
                "era": g.get("home_era", 0.00),
                "whip": g.get("home_whip", 0.00),
                "logo": g.get("home_logo", ""),
                "colors": g.get("home_colors", {"primary": "#111827"}),
            })

        if away_pitcher != "TBD":
            pitchers_list.append({
                "name": away_pitcher,
                "team": away,
                "era": g.get("away_era", 0.00),
                "whip": g.get("away_whip", 0.00),
                "logo": g.get("away_logo", ""),
                "colors": g.get("away_colors", {"primary": "#111827"}),
            })

    # -----------------------------
    # 3. TRENDS (stadium, weather, momentum, streaks)
    # -----------------------------
    try:
        trends = fetch_trends()
    except Exception:
        trends = {
            "stadium_factors": [],
            "weather_factors": [],
            "momentum": [],
            "league_scoring_trends": {},
            "team_streaks": [],
        }

    # -----------------------------
    # 4. HITTERS LEADERBOARD (REAL STATS)
    # -----------------------------
    try:
        hitters_leaderboard = build_hitters_leaderboard(games)
        top_hitters = hitters_leaderboard[:3]
    except Exception:
        hitters_leaderboard = []
        top_hitters = []

    # -----------------------------
    # 5. FINAL PAYLOAD
    # -----------------------------
    return {
        "matchups": matchups,
        "hitters": hitters_leaderboard,
        "top_hitters": top_hitters,
        "pitchers": pitchers_list,
        "stadium_factors": trends["stadium_factors"],
        "weather_factors": trends["weather_factors"],
        "momentum": trends["momentum"],
        "league_scoring_trends": trends["league_scoring_trends"],
        "team_streaks": trends["team_streaks"],
    }
