# scoring.py

def score_hitter(hitter, pitcher_name, stadium_hr_factor):
    """
    Computes the full hitter score including:
    - BvP HR points (0–6)
    - BvP AVG points (0–3)
    - Hit streak points (0–12)
    - Ballpark HR Factor points (0–4)
    - Raw score (0–25)
    - Final normalized score (0–100)
    """

    # -----------------------------
    # 1. BvP HR Points (0–6)
    # -----------------------------
    bvp_hr = hitter.get("bvp_hr", 0)
    bvp_hr_points = min(bvp_hr * 2, 6)

    # -----------------------------
    # 2. BvP AVG Points (0–3)
    # -----------------------------
    bvp_avg = hitter.get("bvp_avg", 0.0)
    plate_appearances = hitter.get("bvp_pa", 0)

    if plate_appearances >= 5:
        if bvp_avg >= 0.300:
            bvp_avg_points = 3
        elif bvp_avg >= 0.250:
            bvp_avg_points = 2
        else:
            bvp_avg_points = 1
    else:
        bvp_avg_points = 0

    # -----------------------------
    # 3. Hit Streak Points (0–12)
    # -----------------------------
    streak = hitter.get("streak", 0)
    streak_points = min(streak, 12)

    # -----------------------------
    # 4. Ballpark HR Factor Points (0–4)
    # -----------------------------
    if stadium_hr_factor >= 120:
        ballpark_points = 4
    elif stadium_hr_factor >= 105:
        ballpark_points = 2
    else:
        ballpark_points = 0

    # -----------------------------
    # 5. Raw Score (max = 25)
    # -----------------------------
    raw_score = (
        bvp_hr_points
        + bvp_avg_points
        + streak_points
        + ballpark_points
    )

    # -----------------------------
    # 6. Final Normalized Score (0–100)
    # -----------------------------
    hitter_score = round((raw_score / 25) * 100)

    # -----------------------------
    # 7. Return full breakdown
    # -----------------------------
    return {
        "name": hitter.get("name"),
        "bvp_hr": bvp_hr,
        "bvp_hr_points": bvp_hr_points,
        "bvp_avg": bvp_avg,
        "bvp_avg_points": bvp_avg_points,
        "streak": streak,
        "streak_points": streak_points,
        "ballpark_hr_factor": stadium_hr_factor,
        "ballpark_points": ballpark_points,
        "raw_score": raw_score,
        "hitter_score": hitter_score,
    }
