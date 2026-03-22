# app/services/analytics.py

from typing import Dict, Any


def _clamp(value: float, min_value: float = 0.0, max_value: float = 100.0) -> float:
    return max(min_value, min(max_value, value))


def calculate_pitcher_difficulty(
    pitcher: Dict[str, Any],
    context: Dict[str, Any],
) -> float:
    """
    0 = easy matchup, 100 = brutal matchup
    context expects:
      - park_factor (float, e.g. 1.12)
      - weather_factor (float, e.g. 1.05)
      - momentum_rating (float 0–1)
      - opp_lineup_ops (float, e.g. 0.750)
      - opp_hot_streaks (int, e.g. count of hot hitters)
    pitcher expects:
      - era, whip, k9, opp_avg
    """

    era = float(pitcher.get("era", 4.00))
    whip = float(pitcher.get("whip", 1.30))
    k9 = float(pitcher.get("k9", 8.0))
    opp_avg = float(pitcher.get("opp_avg", 0.250))

    park_factor = float(context.get("park_factor", 1.00))
    weather_factor = float(context.get("weather_factor", 1.00))
    momentum_rating = float(context.get("momentum_rating", 0.5))
    opp_lineup_ops = float(context.get("opp_lineup_ops", 0.720))
    opp_hot_streaks = int(context.get("opp_hot_streaks", 0))

    # 1) Hitter threat (0–100)
    hitter_threat_score = _clamp((opp_lineup_ops * 200.0) + (opp_hot_streaks * 3.0))

    # 2) Stadium factor (0–100) – only boosts difficulty if > 1.0
    stadium_factor_score = _clamp((park_factor - 1.0) * 100.0)

    # 3) Weather factor (0–100) – only boosts difficulty if > 1.0
    weather_factor_score = _clamp((weather_factor - 1.0) * 200.0)

    # 4) Momentum (0–100)
    momentum_score = _clamp(momentum_rating * 100.0)

    # 5) Pitcher vulnerability (0–100)
    v = (
        (era - 3.00) * 10.0 +
        (whip - 1.10) * 40.0 +
        (opp_avg - 0.230) * 300.0 -
        (k9 - 8.0) * 5.0
    )
    pitcher_vulnerability_score = _clamp(v)

    difficulty = (
        hitter_threat_score * 0.40 +
        stadium_factor_score * 0.20 +
        weather_factor_score * 0.10 +
        momentum_score * 0.10 +
        pitcher_vulnerability_score * 0.20
    )

    return round(_clamp(difficulty), 1)


def calculate_hitter_difficulty(
    hitter: Dict[str, Any],
    context: Dict[str, Any],
) -> float:
    """
    0 = easy matchup, 100 = brutal matchup
    context expects:
      - park_factor
      - weather_factor
      - bullpen_strength (0–1, optional)
    hitter expects:
      - vs_pitcher_era, vs_pitcher_whip, vs_pitcher_k9
      - hit_streak (int, positive = hot, negative = cold)
    """

    era = float(hitter.get("vs_pitcher_era", 3.50))
    whip = float(hitter.get("vs_pitcher_whip", 1.20))
    k9 = float(hitter.get("vs_pitcher_k9", 9.0))
    hit_streak = int(hitter.get("hit_streak", 0))

    park_factor = float(context.get("park_factor", 1.00))
    weather_factor = float(context.get("weather_factor", 1.00))
    bullpen_strength = float(context.get("bullpen_strength", 0.5))

    # 1) Pitcher strength (0–100)
    pitcher_strength_score = _clamp(
        (era * 10.0) +
        (k9 * 2.0) +
        (whip * 25.0)
    )

    # 2) Stadium suppression (0–100) – only if park_factor < 1.0
    stadium_suppression_score = _clamp((1.0 - park_factor) * 100.0) if park_factor < 1.0 else 0.0

    # 3) Weather suppression (0–100) – only if weather_factor < 1.0
    weather_suppression_score = _clamp((1.0 - weather_factor) * 200.0) if weather_factor < 1.0 else 0.0

    # 4) Cold streak (0–100) – only penalize if cold
    cold_streak_score = _clamp((5 - hit_streak) * 10.0) if hit_streak < 0 else 0.0

    # 5) Bullpen strength (0–100)
    bullpen_strength_score = _clamp(bullpen_strength * 100.0)

    difficulty = (
        pitcher_strength_score * 0.50 +
        stadium_suppression_score * 0.20 +
        weather_suppression_score * 0.10 +
        cold_streak_score * 0.10 +
        bullpen_strength_score * 0.10
    )

    return round(_clamp(difficulty), 1)
