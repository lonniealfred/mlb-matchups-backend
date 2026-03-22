# app/services/demo_fallback.py

from typing import Dict, Any, List


def get_demo_dashboard() -> Dict[str, Any]:
    """
    Provides a stable fallback dashboard response when ESPN scraping fails.
    This ensures the frontend always receives the correct structure:
    - matchups
    - pitchers
    - hitters
    """

    demo_matchups: List[Dict[str, Any]] = [
        {
            "home_team": "New York Yankees",
            "away_team": "Boston Red Sox",
            "home_logo": "https://a.espncdn.com/i/teamlogos/mlb/500/nyy.png",
            "away_logo": "https://a.espncdn.com/i/teamlogos/mlb/500/bos.png",
            "start_time": "2024-04-01T23:05:00Z",
            "venue": "Yankee Stadium",
            "weather": {
                "temp_f": 62,
                "condition": "Clear",
                "wind_mph": 5
            },
            "analytics": {
                "run_expectancy": 9.1,
                "park_factor": 1.12,
                "weather_factor": 1.05,
                "momentum_rating": 0.7
            },
            "home_pitcher": {
                "name": "Gerrit Cole",
                "era": 2.63,
                "whip": 1.04,
                "k9": 11.2,
                "bb9": 2.1,
                "opp_avg": 0.212
            },
            "away_pitcher": {
                "name": "Brayan Bello",
                "era": 3.81,
                "whip": 1.27,
                "k9": 8.4,
                "bb9": 2.9,
                "opp_avg": 0.245
            }
        },
        {
            "home_team": "Los Angeles Dodgers",
            "away_team": "San Diego Padres",
            "home_logo": "https://a.espncdn.com/i/teamlogos/mlb/500/lad.png",
            "away_logo": "https://a.espncdn.com/i/teamlogos/mlb/500/sd.png",
            "start_time": "2024-04-01T02:10:00Z",
            "venue": "Dodger Stadium",
            "weather": {
                "temp_f": 72,
                "condition": "Partly Cloudy",
                "wind_mph": 3
            },
            "analytics": {
                "run_expectancy": 8.4,
                "park_factor": 1.08,
                "weather_factor": 1.02,
                "momentum_rating": 0.6
            },
            "home_pitcher": {
                "name": "Walker Buehler",
                "era": 3.12,
                "whip": 1.02,
                "k9": 9.7,
                "bb9": 2.4,
                "opp_avg": 0.218
            },
            "away_pitcher": {
                "name": "Joe Musgrove",
                "era": 3.56,
                "whip": 1.14,
                "k9": 8.9,
                "bb9": 2.2,
                "opp_avg": 0.231
            }
        }
    ]

    return {
        "matchups": demo_matchups,
        "pitchers": [],   # You can enrich this