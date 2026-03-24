# app/services/scoring.py

from typing import Dict, Any


def score_hitter(bvp_hrs: int, bvp_avg: float, hit_streak: int) -> Dict[str, Any]:
    """
    Computes a hitter score based on:
    - BvP HRs vs today's pitcher
    - BvP AVG vs today's pitcher
    - Current hit streak

    Returns:
    {
      "score": int,
      "breakdown": {
        "bvp_hrs_points": int,
        "bvp_avg_points": int,
        "hit_streak_points": int,
        "total_points": int,
        "max_points": int
      }
    }
    """

    # -----------------------------
    # 1. BvP HRs → points
    # -----------------------------
    if bvp_hrs <= 0:
        bvp_hrs_points = 0
    elif bvp_hrs == 1:
        bvp_hrs_points = 2
    elif bvp_hrs == 2:
        bvp_hrs_points = 4
    else:
        bvp_hrs_points = 6  # 3+ HRs

    # -----------------------------
    # 2. BvP AVG → points
    # -----------------------------
    if bvp_avg < 0.250:
        bvp_avg_points = 0
    elif 0.250 <= bvp_avg < 0.280:
        bvp_avg_points = 1
    elif 0.280 <= bvp_avg < 0.300:
        bvp_avg_points = 2
    elif 0.300 <= bvp_avg < 0.350:
        bvp_avg_points = 3
    else:
        bvp_avg_points = 4  # .350+

    # -----------------------------
    # 3. Hit streak → points
    # -----------------------------
    hit_streak_points = max(hit_streak, 0)

    total_points = bvp_hrs_points + bvp_avg_points + hit_streak_points
    max_points = 6 + 4 + 10  # example cap: 10-game streak

    # Normalize to 100‑scale score
    score = int((total_points / max_points) * 100)

    return {
        "score": score,
        "breakdown": {
            "bvp_hrs_points": bvp_hrs_points,
            "bvp_avg_points": bvp_avg_points,
            "hit_streak_points": hit_streak_points,
            "total_points": total_points,
            "max_points": max_points,
        },
    }
