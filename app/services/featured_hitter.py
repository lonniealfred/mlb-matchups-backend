"""
featured_hitter.py

Selects the best available hitter for a given team from the
league-wide hitter rankings. This module is used by the
dashboard builder to attach featured hitters to each matchup.
"""

def pick_featured_hitter(team_name: str, hitter_rankings: list):
    """
    Returns the highest-ranked hitter for the given team.

    hitter_rankings is expected to contain objects like:
    {
        "name": "Aaron Judge",
        "team": "Yankees",
        "avg": ".333",
        "hr": 3,
        "player_id": 33192,
        "score": 94
    }
    """

    if not hitter_rankings:
        return {"name": "TBD", "avg": None, "hr": None, "player_id": None}

    # Filter hitters belonging to this team
    team_hitters = [h for h in hitter_rankings if h.get("team") == team_name]

    # If no hitters found for this team, return placeholder
    if not team_hitters:
        return {"name": "TBD", "avg": None, "hr": None, "player_id": None}

    # Sort by score descending (your ranking system)
    team_hitters.sort(key=lambda h: h.get("score", 0), reverse=True)

    top = team_hitters[0]

    # Return only the fields the frontend needs
    return {
        "name": top.get("name"),
        "avg": top.get("avg"),
        "hr": top.get("hr"),
        "player_id": top.get("player_id"),
    }
