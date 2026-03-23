# app/services/dashboard_live.py
from app.scrapers.mlb_scoreboard import fetch_scoreboard
from app.scrapers.mlb_stats import fetch_team_hit_leaders

TEAM_LOGOS = {
  "Yankees": "https://a.espncdn.com/i/teamlogos/mlb/500/nyy.png",
  # ...
}
TEAM_COLORS = {
  "Yankees": {"primary": "#132448"},
  # ...
}

def build_live_dashboard():
  games_raw = fetch_scoreboard()

  matchups = []
  hitters_leaderboard = []

  for g in games_raw:
    home = g["home_team"]
    away = g["away_team"]

    home_hitters = fetch_team_hit_leaders("NYY")  # map team name → abbr
    away_hitters = fetch_team_hit_leaders("BOS")

    home_featured = home_hitters[0] if home_hitters else None
    away_featured = away_hitters[0] if away_hitters else None

    matchups.append({
      "game_id": f"{home}-{away}",
      "home_team": home,
      "away_team": away,
      "home_logo": TEAM_LOGOS.get(home, ""),
      "away_logo": TEAM_LOGOS.get(away, ""),
      "home_featured_hitter": home_featured,
      "away_featured_hitter": away_featured,
      "home_pitcher": g.get("home_pitcher"),
      "away_pitcher": g.get("away_pitcher"),
      "game_time": g["game_time"],
      "home_colors": TEAM_COLORS.get(home, {"primary": "#111827"}),
      "away_colors": TEAM_COLORS.get(away, {"primary": "#111827"}),
    })

    # You can also push into hitters_leaderboard here with scoring logic

  return {
    "matchups": matchups,
    "hitters": hitters_leaderboard,
    "top_hitters": hitters_leaderboard[:3],
    "pitchers": [],
    "stadium_factors": [],
    "momentum": [],
    "weather_factors": [],
    "league_scoring_trends": {},
    "team_streaks": [],
  }
