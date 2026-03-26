"""
dashboard_live.py

Builds the full dashboard response:
- Live games enriched with featured hitters + team colors
- Hitter rankings (already scored)
- Stadium HR factor trends
"""

from .team_colors import TEAM_COLORS
from .featured_hitter import pick_featured_hitter


def build_live_dashboard(games, hitter_rankings, stadium_factors):
    """
    games: list of dicts from your schedule scraper
    hitter_rankings: list of dicts from your hitter scoring engine
    stadium_factors: list of dicts from your trends module
    """

    output_games = []

    for g in games:
        home_team = g.get("home_team")
        away_team = g.get("away_team")

        # Featured hitters (highest-ranked hitters per team)
        home_featured = pick_featured_hitter(home_team, hitter_rankings)
        away_featured = pick_featured_hitter(away_team, hitter_rankings)

        # Team colors
        home_colors = TEAM_COLORS.get(home_team, {"primary": "#1e293b"})
        away_colors = TEAM_COLORS.get(away_team, {"primary": "#1e293b"})

        # Build enriched game object
        output_games.append({
            "game_id": g.get("game_id"),
            "home_team": home_team,
            "away_team": away_team,

            "home_logo": g.get("home_logo"),
            "away_logo": g.get("away_logo"),

            "home_pitcher": g.get("home_pitcher"),
            "away_pitcher": g.get("away_pitcher"),

            "game_time": g.get("game_time"),

            # NEW: Featured hitters
            "home_featured_hitter": home_featured,
            "away_featured_hitter": away_featured,

            # NEW: Team colors
            "home_colors": home_colors,
            "away_colors": away_colors,
        })

    # Final dashboard payload
    return {
        "mode": "live",
        "games": output_games,
        "hitters": hitter_rankings,
        "trends": stadium_factors,
    }
