# app/services/scoring.py

from typing import List, Dict

def compute_bvp_points(hitter: Dict) -> float:
    """Basic placeholder BvP scoring."""
    avg = hitter.get("avg", 0.0)
    hr = hitter.get("hr", 0)
    return (avg * 10) + (hr * 2)


def compute_streak_points(hitter: Dict) -> float:
    """Reward hot hitters."""
    streak = hitter.get("streak", 0)
    return min(streak * 1.5, 10)  # cap streak bonus


def compute_ballpark_factor(hitter: Dict) -> float:
    """Placeholder ballpark factor (can be replaced with real data)."""
    return 1.0  # neutral for now


def score_hitter(hitter: Dict) -> Dict:
    """Compute full hitter score."""
    bvp = compute_bvp_points(hitter)
    streak = compute_streak_points(hitter)
    park = compute_ballpark_factor(hitter)

    raw = bvp + streak
    final = raw * park

    hitter["score"] = {
        "bvp_hr_points": bvp,
        "bvp_avg_points": bvp,
        "hit_streak_points": streak,
        "ballpark_hr_factor": park,
        "raw_score": raw,
        "final_score": round(final, 1),
    }

    return hitter


def score_hitters(hitters: List[Dict]) -> List[Dict]:
    """Score all hitters safely."""
    return [score_hitter(h) for h in hitters]
