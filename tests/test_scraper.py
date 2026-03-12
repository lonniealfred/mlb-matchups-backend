# tests/test_scraper.py

import pytest
from unittest.mock import patch

from app.services.scraper import (
    get_today_games,
    get_pitcher_stats,
    get_lineup_from_competitor,
    get_bvp_stats,
    get_hit_streak,
    get_stadium_hr_factor,
)


# ---------------------------------------------------------
# Helpers for mocking ESPN JSON responses
# ---------------------------------------------------------

def mock_json(data):
    """Helper to return a function that mocks get_json()."""
    return lambda url: data


# ---------------------------------------------------------
# Test: Stadium HR factor
# ---------------------------------------------------------

def test_stadium_hr_factor_parsing():
    mock_data = {
        "statistics": [
            {"name": "homeRunParkFactor", "value": 115}
        ]
    }

    with patch("app.services.scraper.get_json", mock_json(mock_data)):
        result = get_stadium_hr_factor("123")
        assert result == 115


def test_stadium_hr_factor_missing():
    with patch("app.services.scraper.get_json", mock_json({})):
        result = get_stadium_hr_factor("123")
        assert result == 100  # fallback


# ---------------------------------------------------------
# Test: Pitcher stats parsing
# ---------------------------------------------------------

def test_pitcher_stats_parsing():
    mock_data = {
        "season": {"era": 3.55},
        "last3": {"earnedRuns": 2.0},
        "splits": {"vsOppHand": {"ops": 0.720}},
        "vsTeam": {"era": 4.10}
    }

    probable = {"athlete": {"id": "999", "displayName": "Test Pitcher"}}

    with patch("app.services.scraper.get_json", mock_json(mock_data)):
        result = get_pitcher_stats(probable)

        assert result["name"] == "Test Pitcher"
        assert result["era"] == 3.55
        assert result["recent_er"] == 2.0
        assert result["split_ops"] == 0.720
        assert result["era_vs_team"] == 4.10


def test_pitcher_stats_missing_probable():
    result = get_pitcher_stats({})
    assert result["name"] == "Unknown"
    assert result["era"] == 4.00


# ---------------------------------------------------------
# Test: Lineup parsing
# ---------------------------------------------------------

def test_lineup_parsing():
    competitor = {
        "lineups": [
            {
                "athlete": {"id": "101", "displayName": "Player A"},
                "order": 1,
                "position": "CF"
            },
            {
                "athlete": {"id": "102", "displayName": "Player B"},
                "order": 2,
                "position": "RF"
            }
        ]
    }

    lineup = get_lineup_from_competitor(competitor)

    assert len(lineup) == 2
    assert lineup[0]["name"] == "Player A"
    assert lineup[1]["id"] == "102"


# ---------------------------------------------------------
# Test: BvP stats
# ---------------------------------------------------------

def test_bvp_stats_parsing():
    mock_data = {
        "homeRuns": 2,
        "battingAverage": 0.333,
        "plateAppearances": 12
    }

    with patch("app.services.scraper.get_json", mock_json(mock_data)):
        result = get_bvp_stats("123", "456")

        assert result["hr"] == 2
        assert result["avg"] == 0.333
        assert result["pa"] == 12


def test_bvp_stats_missing_pitcher():
    result = get_bvp_stats("123", None)
    assert result["hr"] == 0
    assert result["avg"] == 0.250


# ---------------------------------------------------------
# Test: Hit streak
# ---------------------------------------------------------

def test_hit_streak_parsing():
    mock_data = {"currentHitStreak": 7}

    with patch("app.services.scraper.get_json", mock_json(mock_data)):
        result = get_hit_streak("123")
        assert result == 7


def test_hit_streak_missing():
    with patch("app.services.scraper.get_json", mock_json({})):
        result = get_hit_streak("123")
        assert result == 0


# ---------------------------------------------------------
# Test: Full game parsing (top-level)
# ---------------------------------------------------------

def test_get_today_games_structure():
    mock_scoreboard = {
        "events": [
            {
                "id": "999",
                "date": "2026-03-09T19:05:00Z",
                "competitions": [
                    {
                        "competitors": [
                            {
                                "team": {"abbreviation": "NYY"},
                                "probables": [{"athlete": {"id": "1", "displayName": "Pitcher A"}}],
                                "lineups": []
                            },
                            {
                                "team": {"abbreviation": "BOS"},
                                "probables": [{"athlete": {"id": "2", "displayName": "Pitcher B"}}],
                                "lineups": []
                            }
                        ],
                        "venue": {"id": "10", "fullName": "Fenway Park"}
                    }
                ]
            }
        ]
    }

    # Mock all dependent calls
    with patch("app.services.scraper.get_json", mock_json(mock_scoreboard)):
        games = get_today_games()

    assert len(games) == 1
    g = games[0]

    assert g["game_id"] == 999
    assert g["away_team"] == "NYY"
    assert g["home_team"] == "BOS"
    assert "pitchers" in g
    assert "hitters" in g
    assert "stadium" in g
