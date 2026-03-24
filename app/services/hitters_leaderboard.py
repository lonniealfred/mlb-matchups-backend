# app/services/hitters_leaderboard.py

from typing import List, Dict, Any

from app.scrapers.mlb_hitters import fetch_featured_hitters
from app.scrapers.mlb_bvp import fetch_bvp
from app.scrapers.mlb_streaks import fetch_hit_streak
from app.scrapers.mlb_season_stats import fetch_season_stats

from app.data.player_data import get_player_id
from app.data.team_data import get_team_logo, get_team_colors

from app.services.scoring import score_hitter


def build_hitters_leaderboard(games: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Builds a league-wide hitters leaderboard using:
    - Featured hitters per game
    - BvP HRs vs today's pitcher
    - BvP AVG vs today's pitcher
    - Current hit streak
    - Season AVG + HR
    - Scoring engine

    Returns a sorted list of hitters with full scoring breakdown.
    """

    leaderboard: List[Dict[str, Any]] = []

    for g in games:
        home_team = g.get("home_team", "TBD")
        away_team = g.get("away_team", "TBD")

        # Get featured hitters for each side
        try:
            home_hitter, away_hitter = fetch_featured_hitters(home_team, away_team)
        except Exception:
            home_hitter = {"name": "TBD", "team": home_team, "avg": ".---", "hr": 0}
            away_hitter = {"name": "TBD", "team": away_team, "avg": ".---", "hr": 0}

        # Normalize hitter objects
        hitters = [
            {
                "name": home_hitter.get("name", "TBD"),
                "team": home_team,
            },
            {
                "name": away_hitter.get("name", "TBD"),
                "team": away_team,
            },
        ]

        # Pitcher names (for BvP pairing)
        home_pitcher_name = g.get("home_pitcher", "TBD")
        away_pitcher_name = g.get("away_pitcher", "TBD")

        for hitter in hitters:
            hitter_name = hitter["name"]
            team = hitter["team"]

            # Skip completely unknown hitters
            if hitter_name == "TBD":
                leaderboard.append(_default_leaderboard_entry(hitter_name, team))
                continue

            # Map hitter + opposing pitcher to ESPN IDs
            hitter_id = get_player_id(hitter_name)
            if team == home_team:
                opposing_pitcher_name = away_pitcher_name
            else:
                opposing_pitcher_name = home_pitcher_name

            pitcher_id = get_player_id(opposing_pitcher_name) if opposing_pitcher_name != "TBD" else None

            # Defaults
            bvp_hrs = 0
            bvp_avg = 0.000
            hit_streak = 0
            season_avg = 0.000
            season_hr = 0

            # BvP
            if hitter_id and pitcher_id:
                try:
                    bvp = fetch_bvp(hitter_id, pitcher_id)
                    bvp_hrs = bvp.get("bvp_hrs", 0)
                    bvp_avg = bvp.get("bvp_avg", 0.000)
                except Exception:
                    pass

            # Hit streak
            if hitter_id:
                try:
                    hit_streak = fetch_hit_streak(hitter_id)
                except Exception:
                    pass

            # Season stats
            if hitter_id:
                try:
                    season = fetch_season_stats(hitter_id)
                    season_avg = season.get("avg", 0.000)
                    season_hr = season.get("hr", 0)
                except Exception:
                    pass

            # Score hitter
            scoring = score_hitter(
                bvp_hrs=bvp_hrs,
                bvp_avg=round(bvp_avg, 3),
                hit_streak=hit_streak,
            )

            leaderboard.append({
                "name": hitter_name,
                "team": team,
                "avg": _format_avg(season_avg),
                "hr": season_hr,
                "score": scoring["score"],
                "breakdown": scoring["breakdown"],
                "bvp_hrs": bvp_hrs,
                "bvp_avg": round(bvp_avg, 3),
                "hit_streak": hit_streak,
                "logo": get_team_logo(team),
                "colors": get_team_colors(team),
            })

    # Sort by score descending
    leaderboard.sort(key=lambda x: x["score"], reverse=True)

    return leaderboard


def _format_avg(avg: float) -> str:
    """
    Formats a float AVG (e.g. 0.287) into a display string ('.287').
    """
    try:
        return f".{int(round(avg * 1000)):03d}"
    except Exception:
        return ".---"


def _default_leaderboard_entry(name: str, team: str) -> Dict[str, Any]:
    """
    Safe fallback entry when we can't resolve IDs or stats.
    """
    return {
        "name": name,
        "team": team,
        "avg": ".---",
        "hr": 0,
        "score": 0,
        "breakdown": {
            "bvp_hrs_points": 0,
            "bvp_avg_points": 0,
            "hit_streak_points": 0,
            "total_points": 0,
            "max_points": 1,
        },
        "bvp_hrs": 0,
        "bvp_avg": 0.000,
        "hit_streak": 0,
        "logo": get_team_logo(team),
        "colors": get_team_colors(team),
    }
