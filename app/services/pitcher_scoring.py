# -------------------------
# Pitcher Ranking System
# Rule #1 — Opponent Team AVG Penalty
# Rule #2 — Last 5 Games ERA Score
# Rule #3 — Stadium Environment Bonus/Penalty
# Rule #4 — Strikeout Average in Last 4 Games
# -------------------------

def rule1_opponent_team_avg(team_avg: float) -> int:
    """
    Rule #1:
    - If opponent AVG >= .250 → 0 points
    - If opponent AVG < .250 → 1 point + 2 points per .020 below .250
    """
    if team_avg >= 0.250:
        return 0

    diff = 0.250 - team_avg
    extra_steps = int(diff // 0.020)
    return 1 + (extra_steps * 2)


def rule2_last5_era(era_last5: float) -> int:
    """
    Rule #2:
    - ERA < 1.50 → +3 points
    - ERA ≤ 2.50 → +2 points
    - ERA ≤ 3.00 → +1 point
    - ERA > 5.00 → -1 point
    - Otherwise → 0 points
    """
    if era_last5 < 1.50:
        return 3
    if era_last5 <= 2.50:
        return 2
    if era_last5 <= 3.00:
        return 1
    if era_last5 > 5.00:
        return -1
    return 0


def rule3_stadium_factor(hr_factor: float) -> int:
    """
    Rule #3:
    - HR factor < 100 → +1 point (pitcher-friendly)
    - HR factor > 100 → -1 point (hitter-friendly)
    - HR factor == 100 → 0 points (neutral)
    """
    if hr_factor < 100:
        return 1
    if hr_factor > 100:
        return -1
    return 0


def rule4_last4_strikeouts(avg_k_last4: float) -> int:
    """
    Rule #4:
    - 5 strikeouts per game average → 5 points
    - +1 additional point for every strikeout above 5
    """
    if avg_k_last4 < 5:
        return 0

    base = 5
    extra = int(avg_k_last4 - 5)
    return base + extra


# -------------------------
# Unified Pitcher Score Engine
# -------------------------

def compute_pitcher_score(p: dict) -> dict:
    """
    Computes the full pitcher score using Rules 1–4.
    Expects a pitcher stats dict with safe defaults.
    """

    # Extract stats with safe defaults
    team_avg = p.get("opponent_team_avg", 0.250)
    era_last5 = p.get("era_last5", 4.50)
    hr_factor = p.get("hr_factor", 100)
    avg_k_last4 = p.get("avg_k_last4", 4.0)

    # Apply rules
    r1 = rule1_opponent_team_avg(team_avg)
    r2 = rule2_last5_era(era_last5)
    r3 = rule3_stadium_factor(hr_factor)
    r4 = rule4_last4_strikeouts(avg_k_last4)

    total = r1 + r2 + r3 + r4

    return {
        "total": total,
        "rule1_opponent_avg": r1,
        "rule2_last5_era": r2,
        "rule3_stadium_factor": r3,
        "rule4_last4_k": r4,
    }
