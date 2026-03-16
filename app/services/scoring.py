# -----------------------------
# PITCHER SCORING
# -----------------------------

def score_pitcher(p):
    if p is None:
        return {
            "name": "Demo Pitcher",
            "era": 3.50,
            "whip": 1.15,
            "hand": "R",
            "pitcher_score": 75
        }

    era = float(p.get("era", 4.00))
    whip = float(p.get("whip", 1.30))

    # Simple normalized scoring
    score = max(0, 100 - (era * 10 + whip * 15))

    return {
        **p,
        "pitcher_score": int(score)
    }


# -----------------------------
# HITTER SCORING
# -----------------------------

def score_hitter(h, pitcher):
    if h is None:
        return {
            "name": "Demo Hitter",
            "avg": .280,
            "hr": 4,
            "rbi": 10,
            "hitter_score": 80
        }

    avg = float(h.get("avg", 0))
    hr = int(h.get("hr", 0))
    rbi = int(h.get("rbi", 0))

    # Pitcher influence
    pitcher_penalty = 0
    if pitcher:
        pitcher_penalty = float(pitcher.get("era", 4.00)) * 2

    # Simple scoring model
    raw = (
        avg * 100 +
        hr * 5 +
        rbi * 1 -
        pitcher_penalty
    )

    score = max(0, min(100, raw))

    return {
        **h,
        "hitter_score": int(score)
    }
