"""
hitters.py

Builds the full hitter ranking list used by:
- Top Hitters tab
- Featured hitters in matchups
- Scoring engine
"""

from typing import List, Dict


def build_hitter_rankings(raw_stats: List[Dict], player_id_map: Dict):
    """
    raw_stats: list of dicts from your stats scraper, shaped like:
    {
        "name": "Aaron Judge",
        "team": "Yankees",
        "avg": 0.333,
        "hr": 3,
        "ops": 1.012,
        "bvp_hr": 1,
        "bvp_avg": 0.250,
        "streak": 5,
        "ballpark_hr_factor": 1.22
    }

    player_id_map: dict mapping player names → ESPN player IDs
    """

    hitters = []

    for p in raw_stats:
        name = p.get("name")
        team = p.get("team")

        # Extract stats
        avg = p.get("avg")
        hr = p.get("hr")
        ops = p.get("ops")

        bvp_hr = p.get("bvp_hr", 0)
        bvp_avg = p.get("bvp_avg", 0)
        streak = p.get("streak", 0)
        ballpark_factor = p.get("ballpark_hr_factor", 1.0)

        # Scoring model (customizable)
        bvp_hr_points = bvp_hr * 2
        bvp_avg_points = bvp_avg * 10
        streak_points = streak * 0.5
        ballpark_points = (ballpark_factor - 1.0) * 10
        season_points = (ops or 0) * 10

        hitter_score = (
            bvp_hr_points +
            bvp_avg_points +
            streak_points +
            ballpark_points +
            season_points
        )

        hitters.append({
            "name": name,
            "team": team,

            # Display stats
            "avg": f"{avg:.3f}" if avg is not None else None,
            "hr": hr,
            "ops": ops,

            # Scoring breakdown
            "bvp_hr": bvp_hr,
            "bvp_hr_points": bvp_hr_points,
            "bvp_avg": bvp_avg,
            "bvp_avg_points": bvp_avg_points,
            "streak": streak,
            "streak_points": streak_points,
            "ballpark_hr_factor": ballpark_factor,
            "ballpark_points": ballpark_points,
            "season_points": season_points,

            # Final score
            "score": round(hitter_score, 2),

            # ESPN headshot support
            "player_id": player_id_map.get(name)
        })

    # Sort by score descending
    hitters.sort(key=lambda h: h["score"], reverse=True)

    return hitters
