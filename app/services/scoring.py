def score_hitter(hitter, pitcher):
    if pitcher is None:
        return {
            **hitter,
            "bvp_hr": 0,
            "bvp_avg": 0,
            "streak": 0,
            "ballpark_hr_factor": 100,
            "raw_score": 0,
            "hitter_score": 0
        }

    # Placeholder BVP logic (real version uses ESPN BVP data)
    bvp_hr = 0
    bvp_avg = hitter.get("avg", 0)

    # Simple streak placeholder
    streak = hitter.get("hr", 0)

    # Ballpark factor placeholder
    ballpark_factor = 100

    raw = (
        (bvp_hr * 2) +
        (bvp_avg * 10) +
        (streak * 1) +
        (ballpark_factor / 25)
    )

    return {
        **hitter,
        "bvp_hr": bvp_hr,
        "bvp_avg": bvp_avg,
        "streak": streak,
        "ballpark_hr_factor": ballpark_factor,
        "raw_score": raw,
        "hitter_score": int(raw * 4)
    }
