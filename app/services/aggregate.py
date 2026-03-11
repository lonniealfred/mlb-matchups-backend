# app/services/aggregate.py

from app.services.scoring import (
    score_batter_vs_pitcher,
    score_hit_streak,
    score_stadium,
    score_pitcher_vulnerability
)

def compute_hitter_score(hitter):
    bvp = score_batter_vs_pitcher(
        hr=hitter["hr_vs_pitcher"],
        avg=hitter["avg_vs_pitcher"],
        pa=hitter["pa_vs_pitcher"]
    )

    streak = score_hit_streak(hitter["streak"])

    return bvp + streak


def compute_team_offense(top_hitters, opposing_pitcher):
    hitter_scores = [compute_hitter_score(h) for h in top_hitters]
    hitter_total = sum(hitter_scores)

    pitcher_score = score_pitcher_vulnerability(
        era=opposing_pitcher["era"],
        recent_er=opposing_pitcher["recent_er"],
        split_ops=opposing_pitcher["split_ops"],
        era_vs_team=opposing_pitcher.get("era_vs_team")
    )

    return hitter_total + pitcher_score


def compute_game_score(game):
    stadium_score = score_stadium(game["stadium"]["hr_factor"])

    away_score = compute_team_offense(
        game["hitters"]["away_top_hitters"],
        game["pitchers"]["home_pitcher"]
    )

    home_score = compute_team_offense(
        game["hitters"]["home_top_hitters"],
        game["pitchers"]["away_pitcher"]
    )

    return away_score + home_score + stadium_score
