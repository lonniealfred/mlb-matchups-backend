# app/services/scoring.py

def score_batter_vs_pitcher(hr: int, avg: float, pa: int) -> float:
    score = 0
    score += hr  # 1 point per HR

    if pa >= 5:
        score += avg * 10  # scaled AVG rule

    return score


def score_hit_streak(streak: int) -> int:
    if streak >= 11:
        return 20
    elif streak >= 8:
        return 15
    elif streak >= 6:
        return 10
    elif streak >= 4:
        return 5
    return 0


def score_stadium(hr_factor: float) -> float:
    return (hr_factor - 100) / 2


def score_pitcher_vulnerability(era: float, recent_er: float, split_ops: float, era_vs_team=None) -> float:
    score = 0

    # Season ERA
    if era >= 6: score += 10
    elif era >= 5: score += 8
    elif era >= 4: score += 5
    elif era >= 3.5: score += 3

    # Recent form
    if recent_er >= 5: score += 6
    elif recent_er >= 4: score += 4
    elif recent_er >= 3: score += 2

    # Splits
    if split_ops >= .800: score += 4
    elif split_ops >= .750: score += 2

    # Team history
    if era_vs_team is not None:
        if era_vs_team >= 5: score += 3
        elif era_vs_team >= 4: score += 1

    return min(score, 20)
