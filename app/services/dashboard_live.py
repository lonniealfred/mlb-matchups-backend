# app/services/dashboard_live.py

from app.scrapers.mlb_scoreboard import fetch_scoreboard
from app.scrapers.mlb_pitchers import fetch_pitchers_for_game
from app.scrapers.mlb_hitters import fetch_featured_hitters
from app.scrapers.mlb_trends import fetch_trends

from app.services.hitters_leaderboard import build_hitters_leaderboard

# Demo fallback data
from app.demo.demo_games import DEMO_GAMES
from app.demo.demo_hitters import DEMO_HITTERS
from app.demo.demo_trends import DEMO_TRENDS


# ---------------------------------------------------------
# MODE DETECTION (used by /mode endpoint)
# ---------------------------------------------------------
def get_dashboard_mode():
    """
    Returns 'live' if MLB scoreboard has real games.
    Returns 'demo' if using fallback demo data.
    """
    try:
        games = fetch_scoreboard()
    except Exception:
        return "demo"

    return "live" if games else "demo"


# ---------------------------------------------------------
# MAIN DASHBOARD BUILDER
# ---------------------------------------------------------
def build_live_dashboard():
    """
    Builds the full live dashboard payload.
    Always returns full cards, even when MLB has no games.
    """

    # 1. SCOREBOARD
    try:
        games = fetch_scoreboard()
    except Exception:
        games = []

    # If no real games → use demo placeholders
    if not games:
        games = DEMO_GAMES

    matchups = []
    pitchers_list = []

    # 2. PROCESS EACH GAME
    for g in games:
        home = g.get("home_team", "TBD")
        away = g.get("away_team", "TBD")

        # Pitchers
        try:
            home_pitcher, away_pitcher = fetch_pitchers_for_game(home, away)
        except Exception:
            home_pitcher = g.get("home_pitcher", "TBD")
            away_pitcher = g.get("away_pitcher", "TBD")

        # Featured hitters
        try:
            home_hitter, away_hitter = fetch_featured_hitters(home, away)
        except Exception:
            home_hitter = g.get("home_featured_hitter", {"name": "TBD"})
            away_hitter = g.get("away_featured_hitter", {"name": "TBD"})

        # Matchup card
        matchups.append({
            "game_id": g.get("game_id"),
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

        # Pitchers tab
        pitchers_list.append({
            "name": home_pitcher,
            "team": home,
            "era": g.get("home_era", 0.00),
            "whip": g.get("home_whip", 0.00),
            "logo": g.get("home_logo", ""),
            "colors": g.get("home_colors", {"primary": "#111827"}),
        })

        pitchers_list.append({
            "name": away_pitcher,
            "team": away,
            "era": g.get("away_era", 0.00),
            "whip": g.get("away_whip", 0.00),
            "logo": g.get("away_logo", ""),
            "colors": g.get("away_colors", {"primary": "#111827"}),
        })

    # 3. TRENDS
    try:
        trends = fetch_trends()
    except Exception:
        trends = DEMO_TRENDS

    if not trends.get("stadium_factors"):
        trends = DEMO_TRENDS

    # 4. HITTERS LEADERBOARD
    try:
        hitters_leaderboard = build_hitters_leaderboard(games)
    except Exception:
        hitters_leaderboard = []

    if not hitters_leaderboard:
        hitters_leaderboard = DEMO_HITTERS

    top_hitters = hitters_leaderboard[:3]

    # 5. FINAL PAYLOAD
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
