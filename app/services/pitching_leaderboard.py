from .pitcher_scoring import compute_pitcher_score

def build_pitching_leaderboard(raw_pitchers: list[dict]) -> list[dict]:
    leaderboard = []

    for p in raw_pitchers:
        score = compute_pitcher_score(p)

        leaderboard.append({
            "name": p.get("name"),
            "team": p.get("team"),
            "opponent": p.get("opponent"),
            "opponent_team_avg": p.get("opponent_team_avg"),
            "era_last5": p.get("era_last5"),
            "hr_factor": p.get("hr_factor"),
            "avg_k_last4": p.get("avg_k_last4"),
            "score": score["total"],
            "score_breakdown": score,
        })

    # highest score first
    leaderboard.sort(key=lambda x: x["score"], reverse=True)
    return leaderboard
