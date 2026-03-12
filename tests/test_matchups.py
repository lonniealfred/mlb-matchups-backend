# tests/test_matchups.py

import pytest
from unittest.mock import patch

from app.services.matchups import build_matchup_objects
from app.schemas import Game


# ---------------------------------------------------------
# Mock raw scraped game data
# ---------------------------------------------------------

MOCK_SCRAPED_GAMES = [
    {
        "game_id": 999,
        "start_time": "2026-03-09T19:05:00",
        "away_team": "NYY",
        "home_team": "BOS",

        "stadium": {
            "name": "Fenway Park",
            "hr_factor": 115
        },

        "pitchers": {
            "away_pitcher": {
                "name": "Pitcher A",
                "era": 3.55,
                "recent_er": 2.0,
                "split_ops": 0.720,
                "era_vs_team": 4.10,
                "id": "1"
            },
            "home_pitcher": {
                "name": "Pitcher B",
                "era": 4.20,
                "recent_er": 3.0,
                "split_ops": 0.760,
                "era_vs_team": 4.80,
                "id": "2"
            }
        },

        "hitters": {
            "away_top_hitters": [
                {"name": "Judge", "hr_vs_pitcher": 2, "avg_vs_pitcher": 0.333, "pa_vs_pitcher": 12, "streak": 5}
            ],
            "home_top_hitters": [
                {"name": "Devers", "hr_vs_pitcher": 1, "avg_vs_pitcher": 0.280, "pa_vs_pitcher": 10, "streak": 3}
            ]
        }
    }
]


# ---------------------------------------------------------
# Test: Full matchup assembly
# ---------------------------------------------------------

def test_build_matchup_objects():
    with patch("app.services.matchups.get_today_games", return_value=MOCK_SCRAPED_GAMES):
        games = build_matchup_objects()

    assert len(games) == 1
    game = games[0]

    assert isinstance(game, Game)
    assert game.game_id == 999
    assert game.away_team == "NYY"
    assert game.home_team == "BOS"

    # Stadium
    assert game.stadium.name == "Fenway Park"
    assert game.stadium.hr_factor == 115

    # Pitchers
    assert game.pitchers.away_pitcher.name == "Pitcher A"
    assert game.pitchers.home_pitcher.era == 4.20

    # Hitters
    assert len(game.hitters.away_top_hitters) == 1
    assert game.hitters.away_top_hitters[0].name == "Judge"

    # Team scores
    assert game.team_scores.away_offense_score is not None
    assert game.team_scores.home_offense_score is not None

    # Final game score
    assert isinstance(game.game_score, float)
