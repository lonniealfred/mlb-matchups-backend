# tests/test_scoring.py

import pytest

from app.services.scoring import (
    score_batter_vs_pitcher,
    score_hit_streak,
    score_pitcher_vulnerability,
    score_stadium_factor
)


# ---------------------------------------------------------
# Batter vs Pitcher scoring
# ---------------------------------------------------------

def test_score_batter_vs_pitcher_basic():
    hitter = {
        "hr_vs_pitcher": 2,
        "avg_vs_pitcher": 0.333,
        "pa_vs_pitcher": 12
    }

    score = score_batter_vs_pitcher(hitter)
    assert score > 0
    assert isinstance(score, float)


def test_score_batter_vs_pitcher_zero_pa():
    hitter = {
        "hr_vs_pitcher": 0,
        "avg_vs_pitcher": 0.0,
        "pa_vs_pitcher": 0
    }

    score = score_batter_vs_pitcher(hitter)
    assert score == 0


# ---------------------------------------------------------
# Hit streak scoring
# ---------------------------------------------------------

def test_score_hit_streak_ranges():
    assert score_hit_streak(0) == 0
    assert score_hit_streak(4) == 5
    assert score_hit_streak(6) == 10
    assert score_hit_streak(8) == 15
    assert score_hit_streak(11) == 20


# ---------------------------------------------------------
# Pitcher vulnerability scoring
# ---------------------------------------------------------

def test_score_pitcher_vulnerability():
    pitcher = {
        "era": 4.50,
        "recent_er": 5.0,
        "split_ops": 0.800,
        "era_vs_team": 5.20
    }

    score = score_pitcher_vulnerability(pitcher)
    assert score > 0
    assert isinstance(score, float)


# ---------------------------------------------------------
# Stadium factor scoring
# ---------------------------------------------------------

def test_score_stadium_factor():
    assert score_stadium_factor(100) == 0
    assert score_stadium_factor(120) > 0
    assert score_stadium_factor(80) < 0
