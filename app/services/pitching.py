"""
pitching.py
Service module for assembling pitcher data and applying the
Pitcher Ranking System (Rules 1–4).
"""

from app.services.pitcher_scoring import compute_pitcher_score


# ---------------------------------------------------------
# Safe default pitcher object (used when ESPN data is missing)
# ---------------------------------------------------------

DEFAULT_PITCHER = {
    "name": "TBD",
    "team": "TBD",
    "opponent_team_avg": 0.250,
    "era_last5": 4.50,
    "hr_factor": 100,
    "avg_k_last4": 4.0,
}


# ---------------------------------------------------------
# Main function: build and score pitchers
# ---------------------------------------------------------

def build_pitcher_object(raw: dict) -> dict:
    """
    Takes raw pitcher data (from ESPN or elsewhere),
    applies safe defaults, computes score, and returns
    a fully enriched pitcher object.
    """

    p = {
        "name": raw.get("name", DEFAULT_PITCHER["name"]),
        "team": raw.get("team", DEFAULT_PITCHER["team"]),

        # Rule 1 input
        "opponent_team_avg": raw.get("opponent_team_avg", DEFAULT_PITCHER["opponent_team_avg"]),

        # Rule 2 input
        "era_last5": raw.get("era_last5", DEFAULT_PITCHER["era_last5"]),

        # Rule 3 input
        "hr_factor": raw.get("hr_factor", DEFAULT_PITCHER["hr_factor"]),

        # Rule 4 input
        "avg_k_last4": raw.get("avg_k_last4", DEFAULT_PITCHER["avg_k_last4"]),
    }

    # Apply scoring engine
    p["score"] = compute_pitcher_score(p)

    return p


# ---------------------------------------------------------
# Public function: return a ranked list of pitchers
# ---------------------------------------------------------

def get_pitching_rankings(raw_pitchers: list) -> list:
    """
    Accepts a list of raw pitcher dicts (from ESPN scraper or demo data),
    converts them into enriched pitcher objects, scores them,
    and returns a sorted list (highest score first).
    """

    pitchers = [build_pitcher_object(p) for p in raw_pitchers]

    # Sort by total score descending
    pitchers.sort(key=lambda x: x["score"]["total"], reverse=True)

    return pitchers


# ---------------------------------------------------------
# Optional: Demo mode (useful for offseason or empty ESPN data)
# ---------------------------------------------------------

def get_demo_pitching():
    """
    Returns a small set of demo pitchers for UI testing.
    """

    demo_raw = [
        {
            "name": "Gerrit Cole",
            "team": "NYY",
            "opponent_team_avg": 0.220,
            "era_last5": 2.10,
            "hr_factor": 95,
            "avg_k_last4": 6.5,
        },
        {
            "name": "Logan Webb",
            "team": "SF",
            "opponent_team_avg": 0.260,
            "era_last5": 3.40,
            "hr_factor": 105,
            "avg_k_last4": 4.8,
        },
    ]

    return get_pitching_rankings(demo_raw)
